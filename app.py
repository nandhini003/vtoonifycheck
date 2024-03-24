from flask import Flask, request, jsonify
from google.cloud import storage
from vtoonify_model import Model
import numpy as np
from PIL import Image
from io import BytesIO
import torch
import os
import yaml








print("hello world")


model = Model(device='cuda' if torch.cuda.is_available() else 'cpu')
print("Invoking Model")
model.load_model('cartoon1')
print("Loading model successful ... ")