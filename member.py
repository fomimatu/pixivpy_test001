# coding: utf-8

"""
作家情報
"""
class artistData:
    def __init__(self):  # デフォルト値
        self.pixivID # フォルダ名は、pixivID + "." + name
        self.name    # 漢字名
        self.acount # ローマ字名
        self.scoreAVG       # TOP10の平均
        self.favoritedAVG
        self.images  # list[imageData]

        self.score   #stats.score
        self.favorited_count #stats.favorited_count.public + tats.favorited_count.private
        self.accessTime = None




"""
画像情報
"""
class imageData:
    def __init__(self):  # デフォルト値
        self.imageID #
        self.title
        self.tags #
        self.score
        self.view_count
        self.favorited_count
        self.created_time

        self.accessTime = None  # 更新時間、ここがNoneなら末巡回とする