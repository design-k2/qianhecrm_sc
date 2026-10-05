# 从 Noto Sans SC 里只截取 index.html 用到的字，生成很小的 woff2 字体。
# 改过页面文字后重新运行一次：
#     pip install fonttools brotli
#     python build-fonts.py <NotoSansSC 字体所在文件夹>
import os
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

here = os.path.dirname(os.path.abspath(__file__))
source = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "qianhe", "src", "Qianhe.Crm.App", "Fonts")

with open(os.path.join(here, "index.html"), encoding="utf-8") as f:
    text = f.read()
# 常用标点和数字字母全部带上，改几个字不必每次都重新生成
chars = sorted(set(text) | set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ，。、；：？！“”‘’（）《》—…·×%.,:;!?-+/()[] "))
chars = [c for c in chars if c >= " "]

for weight in ("Regular", "Bold"):
    font = TTFont(os.path.join(source, "NotoSansSC-%s.ttf" % weight))
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    subsetter = subset.Subsetter(options)
    subsetter.populate(text="".join(chars))
    subsetter.subset(font)
    target = os.path.join(here, "assets", "fonts", "NotoSansSC-%s.subset.woff2" % weight)
    font.flavor = "woff2"
    font.save(target)
    print("%s  %d 个字  %.0f KB" % (os.path.basename(target), len(chars), os.path.getsize(target) / 1024))
