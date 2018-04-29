# coding: utf-8


"""
作家情報
"""
class artistData:
    def __init__(self):  # デフォルト値
        self.pixivID = None  #
        self.name = None    # 漢字名
        self.acount = None  # ローマ字名
        self.avg_views_count = None       # TOP10の平均
        self.avg_favorited_count = None
        self.images = None  # list[imageData]
        self.score = None   #stats.score
        self.favorited_count = None  # stats.favorited_count.public + tats.favorited_count.private
        self.accessTime = None


"""
画像情報
"""
class imageData:
    def __init__(self):  # デフォルト値
        self.imageID = None
        self.pixivID = None
        self.title = None
        self.tags = None
        self.score = None
        self.view_count = None
        self.favorited_count = None
        self.created_time = None
