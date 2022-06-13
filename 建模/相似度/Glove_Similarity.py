from glove import Glove

glove_model = Glove.load('./模型/glove_ALL/glove.model')

print(glove_model.most_similar('VR', 10))
