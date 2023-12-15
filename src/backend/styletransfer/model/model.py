import os
import copy
import random
import shutil
import numpy as np
from glob import glob

# For Image reading and visualization
from PIL import Image

# For Image Optimization
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# For defining loss functions
from torchvision.models import vgg19, VGG19_Weights
import torchvision.transforms as transforms
from torch.backends import cudnn

from .utils import get_input_optimizer, image_preparer
from .modules import ContentLoss, StyleLoss, Normalization

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.set_default_device(device)
print("You are using {} device.".format(device))

random.seed(42)
cudnn.benchmark = True


def get_model_and_losses(style_img,
                         content_img,
                         cnn=vgg19(
                             weights=VGG19_Weights.DEFAULT).features.eval(),
                         normalization_mean=torch.tensor(
                             [0.485, 0.456, 0.406]),
                         normalization_std=torch.tensor([0.229, 0.224, 0.225]),
                         content_layers=['relu_4'],
                         style_layers=['relu_1', 'relu_2', 'relu_3', 'relu_4', 'relu_5']):

    # Normalization module
    normalization = Normalization(normalization_mean, normalization_std)

    # Just to have an iterable access to or list of content/style losses
    content_losses = []
    style_losses = []

    # Assuming that ``cnn`` is a ``nn.Sequential``, so we make a new ``nn.Sequential``
    # to put in modules that are supposed to be activated sequentially
    model = nn.Sequential(normalization)

    i = 0  # increment every time we see a conv
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = 'conv_{}'.format(i)
        elif isinstance(layer, nn.ReLU):
            name = 'relu_{}'.format(i)
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = 'pool_{}'.format(i)
        elif isinstance(layer, nn.BatchNorm2d):
            name = 'bn_{}'.format(i)
        else:
            raise RuntimeError('Unrecognized layer: {}'.format(
                layer.__class__.__name__))

        model.add_module(name, layer)

        if name in content_layers:
            # add content loss:
            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module("content_loss_{}".format(i), content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            # add style loss:
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module("style_loss_{}".format(i), style_loss)
            style_losses.append(style_loss)

    # now we trim off the layers after the last content and style losses
    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]
    return model, style_losses, content_losses


def run_style_transfer(style_img,
                       content_img,
                       input_img,
                       cnn=vgg19(
                           weights=VGG19_Weights.DEFAULT).features.eval(),
                       normalization_mean=torch.tensor([0.485, 0.456, 0.406]),
                       normalization_std=torch.tensor([0.229, 0.224, 0.225]),
                       content_layers=['relu_4'],
                       style_layers=['relu_1', 'relu_2',
                                     'relu_3', 'relu_4', 'relu_5'],
                       num_steps=300,
                       style_weight=1000000,
                       content_weight=1):
    model, style_losses, content_losses = get_model_and_losses(style_img,
                                                               content_img,
                                                               cnn,
                                                               normalization_mean,
                                                               normalization_std,
                                                               content_layers,
                                                               style_layers)

    # We want to optimize the input and not the model parameters so we
    # update all the requires_grad fields accordingly
    input_img.requires_grad_(True)

    # We also put the model in evaluation mode, so that specific layers
    # such as dropout or batch normalization layers behave correctly.
    model.eval()
    model.requires_grad_(False)

    optimizer = get_input_optimizer(input_img)

    run = [0]
    while run[0] <= num_steps:

        def closure():
            # correct the values of updated input image
            with torch.no_grad():
                input_img.clamp_(0, 1)

            optimizer.zero_grad()
            model(input_img)
            style_score = 0
            content_score = 0

            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            run[0] += 1
            if run[0] % 50 == 0:
                print("run {}:".format(run))
                print('Style Loss : {:4f} Content Loss: {:4f}'.format(
                    style_score.item(), content_score.item()))
                print()

            return style_score + content_score

        optimizer.step(closure)

    # a last correction...
    with torch.no_grad():
        input_img.clamp_(0, 1)

    return input_img


def style_transfer(content_image, style_image):
    style_image = style_image.resize(content_image.size)
    
    content_img = image_preparer(content_image, device)
    style_img = image_preparer(style_image, device)

    print(content_img.shape, style_img.shape)

    # input_img = torch.randn_like(content_img)
    input_img = torch.clone(content_img)
    # input_img = torch.clone(style_img)
    # input_img = style_img + torch.randn_like(style_img)
    # input_img = content_img + torch.randn_like(content_img)

    output = run_style_transfer(style_img=style_img,
                                content_img=content_img,
                                input_img=input_img,
                                num_steps=300,
                                style_weight=1000000,
                                content_weight=1)

    image = output.cpu().clone()
    image = image.squeeze(0)
    image = transforms.ToPILImage()(image)
    return image


if __name__ == '__main__':
    content_img = Image.open('test_images/content_image.jpeg')
    # style_img = Image.open('test_images/style_image.jpeg')
    style_img = Image.open('test_images/mottled-landscape-1924.jpg')
    
    print(content_img.size, style_img.size)

    import time
    start_time = time.time()
    stylized_img = style_transfer(
        content_image=content_img, style_image=style_img)
    print(time.time() - start_time)
    stylized_img.save(f'./test_images/stylized_image_{start_time}.jpeg')
