import time
from pixivpy3 import *
import json
from time import sleep
import os
import member as mem
import pickle
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------
def pixiv_get():
    saveDir = "K:/PIXIV/pixiv_images/"
    # ログイン処理
    api = PixivAPI()
    f = open('K:/PIXIV/client.json', 'r')
    client_info = json.load(f)
    f.close()
    # ここに直接アカウント情報を書いても大丈夫です.
    api.login(client_info['pixiv_id'], client_info['password'])

    # ここでIDを指定します.
    STARTID = 88706  # 0 - 32157 :150000 32158 - 56487: 50000, 56478 - 62709 :10000
    ENDID = 1000000

    for ID in range(STARTID, ENDID):
        start = time.time()
        # アーティスト検索から情報取得
        # try:
        artist_pixiv_id = ID



        # ここのper_pageの値を変えることで一人の絵師さんから持ってくる最大数を定義できます.
        json_result = api.users_works(artist_pixiv_id, per_page=3000)
        if json_result.status == 'failure':
            continue

        score_list = [(idx, dic["stats"]["score"]) for idx, dic in enumerate(json_result.response)]
        dic_count = len(score_list)  # max(score_list, key=lambda item:item[1])[0]

        # 僕はscoreが500以上の人を収集対象にしました.
        # よりクオリティの高い画像のみを集めたい場合はこの閾値を変更してください.
        if any(x[1] >= 5000 for x in score_list):  #  150000 50000
            artist = mem.artistData()
            artist.pixivID = ID
            # 絵師の全データより計算
            artist.avg_views_count = round(sum([dic["stats"]["views_count"] for dic in json_result.response]) / dic_count)
            artist.avg_favorited_count = round(sum([dic["stats"]["favorited_count"]["public"] + dic["stats"]["favorited_count"]["private"] for dic in json_result.response]) / dic_count)

            # 最後のデータでアーティスト情報取得
            dic_pixiv = json_result.response[-1]
            dic_user = dic_pixiv["user"]
            artist.name = dic_user["name"]
            artist.account = dic_user["account"]
            artist.accessTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            # pickle保存
            savePath = saveDir + "artist_{0}.pkl".format(ID)
            with open(savePath, 'wb') as sw:
                pickle.dump(artist, sw)

            #スコアが高い３枚をダウンロード
            score_list.sort(key=lambda tup: tup[1], reverse=True)
            # score_list.sort(reverse=True)
            for tpl_score in score_list[0:5]:
                idx = tpl_score[0]
                img_data = json_result.response[idx]
                # データ取得
                img = mem.imageData()
                img.imageID = img_data["id"]
                img.title = img_data["title"]
                img.tags = img_data["tags"]
                img.score = img_data["stats"]["score"]
                img.view_count = img_data["stats"]["views_count"]
                img.favorited_count = (img_data["stats"]["favorited_count"]["public"] + img_data["stats"]["favorited_count"]["private"])
                img.created_time = img_data["created_time"]
                # pickle保存
                savePath = saveDir + "{0}_artist_{1}.pkl".format(img.imageID, ID)
                with open(savePath, 'wb') as sw:
                    pickle.dump(img, sw)

                # 画像ダウンロード
                if not os.path.exists(saveDir):
                    os.mkdir(saveDir)
                api.download(img_data["image_urls"]["large"], saveDir)
                sleep(1)
        print(ID, time.time() - start)








        """
        if score < 500:
            continue

        total_works = json_result.pagination.total
        illust = json_result.response[0]

        # 画像の保存先を定義しています.
        # 特に指定先に希望がない場合はこのままでokです.
        # このまま走らせると, このスクリプトがあるディレクトリの直下に
        # "pixiv_images"フォルダが作成され画像が DLされます.
        if not os.path.exists("K:/PIXIV/pixiv_images"):
            os.mkdir("K:/PIXIV/pixiv_images")
        saving_direcory_path = 'K:/PIXIV/pixiv_images'

        aapi = AppPixivAPI()
        separator = '------------------------------------------------------------'

        # ダウンロード
        print('Artist: %s' % illust.user.name)
        print('Works: %d' % total_works)
        print(separator)

        # 絵師さんごとにディレクトリを分けたい場合は以下の２行を
        # アンコメントアウトしてください.
        # 一つのディレクトリにまとめたい場合はそのままでokです.

        if not os.path.exists(saving_direcory_path):
            os.mkdir(saving_direcory_path)

        for work_no in range(0, total_works):
            illust = json_result.response[work_no]
            print('Procedure: %d/%d:%d' % (work_no + 1, total_works, ID))
            print('Title: %s' % illust.title)
            print(separator)
            aapi.download(illust.image_urls.large, saving_direcory_path)
            sleep(1)

        print('\nThat\'s all.')
     """
    #except Exception as e:
        #print(type(e))
        #continue



# ----------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------
def main():
    start = time.time()

    # まだ始めたばかりなので、とりあえずデフォのスコア５００以上でサイズが大きいのを５枚ずつダウンロードする
    pixiv_get()

    # 処理時間
    print(time.time() - start)

# ----------------------------------------------------------------------------------------------------------
# スタート
# ----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
