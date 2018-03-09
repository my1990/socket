from wordcloud import WordCloud
import jieba
from scipy.misc import imread
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
name = '妖猫传 短评'
f = open(name + '.txt','r',encoding='utf-8')
text = f.read()
f.close()
d = path.dirname(__file__)
cut_text = ' '.join(jieba.cut(text))
color_mask = imread("./20160721185925416.jpg") # 读取背景图片
cloud = WordCloud(font_path='./STXINGKA.TTF',background_color='white',mask=color_mask,max_words=200,max_font_size=80)
word_cloud = cloud.generate(cut_text) # 产生词云

image_colors = ImageColorGenerator(color_mask)

plt.figure()
# 以下代码显示图片
plt.imshow(cloud)
plt.axis("off")
plt.show()
# 绘制词云