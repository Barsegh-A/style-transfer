import torch
import torch.nn as nn

from utils import gram_matrix


class ContentLoss(nn.Module):
    """
    We will add this content loss module directly after the convolution layer(s)
    that are being used to compute the content distance.
    This way each time the network is fed an input image the content losses
    will be computed at the desired layers.
    """

    def __init__(self, target,):
        super(ContentLoss, self).__init__()
        # Since the target for content loss is fixed and is the same feature map
        # of content image, we will assign it during loss initialization.
        self.target = target.detach()

    def forward(self, input):
        """
        To make the content loss layer transparent we must define forward method,
        that computes the content loss and then returns the layer's input.
        The computed loss is saved as a parameter of the module.
        """
        
        self.loss = ((input - self.target)**2).mean()

        # Return the same input, to be able to use ``ContentLoss`` module as NN block.
        # Read the docs and check ``get_model_and_losses`` function first if you are confused.
        return input


class StyleLoss(nn.Module):
    """
    Similar to the ContentLoss module, we will add style loss module directly
    after the convolution layer(s) that are being used to compute the style distance.
    And again, each time the network is fed an input image the style losses
    will be computed at the desired layers.
    """

    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        # Again, since the target for style loss is fixed and is the same gram matrix
        # of style image features, we will assign it during loss initialization.
        self.target = gram_matrix(target_feature).detach()

    def forward(self, input):
        """
        To make the style loss layer transparent we must define forward method,
        that computes the style loss and then returns the layer's input.
        The computed loss is saved as a parameter of the module.
        """

        G = gram_matrix(input)

        self.loss = ((G - self.target)**2).mean()

        # Return the same input, to be able to use ``StyleLoss`` module as NN block.
        # Read the docs and check ``get_model_and_losses`` function first if you are confused.
        return input


class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        # .view the mean and std to make them [C x 1 x 1] so that they can
        # directly work with image Tensor of shape [B x C x H x W].
        # B is batch size. C is number of channels. H is height and W is width.
        self.mean = torch.tensor(mean).view(-1, 1, 1)
        self.std = torch.tensor(std).view(-1, 1, 1)

    def forward(self, img):
        # normalize ``img``
        return (img - self.mean) / self.std


