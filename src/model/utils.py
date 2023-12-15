import torch
import torch.nn as nn
import torchvision.transforms as transforms


def gram_matrix(input):
    a, b, c, d = input.size()
    # a=batch size(=1)
    # b=number of feature maps
    # (c,d)=dimensions of a f. map (N=c*d)

    # Reshape the given I into \hat_I (see the above explanation of style loss)
    features = input.view(a * b, c * d)

    G = features @ features.T

    G = G / (c*d*b)

    return G


def get_input_optimizer(input_img):
    # As suggested in the paper, we will use L-BFGS algorithm to run our gradient descent.

    optimizer = torch.optim.LBFGS([input_img])
    # optimizer = torch.optim.Adam([input_img], lr=0.05)
    return optimizer


def image_preparer(image, device):
    # Convert from PIL Image to Torch Tensor
    image = transforms.ToTensor()(image)

    # Fake batch dimension required to fit network's input dimensions
    image = image.unsqueeze(0)
    return image.to(device, torch.float)