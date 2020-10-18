import requests
import csv


class Bsite(object):

    def __init__(self, cookies):
        """
        一般先登录B站后，将获取到的有效的cookies传入Bsite
        :param cookies:
        """
        self.cookies = cookies
        self.headers = {"referer": "https://www.bilibili.com/",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}



    def aid2bvid(self, aid):
        """
        将aid转为bvid
        :param aid: B站视频链接内的aid号
        :return: 返回bvid
        """
        table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr = {}
        for i in range(58):
            tr[table[i]] = i
        s = [11, 10, 3, 8, 4, 6]
        xor = 177451812
        add = 8728348608
        aid = (aid ^ xor) + add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]] = table[aid // 58 ** i % 58]
        return ''.join(r)

    def bvid2aid(self, bvid):
        """
        将bvid转为aid
        :param bvid: B站视频链接内的bvid号
        :return: aid号
        """
        table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr = {}
        for i in range(58):
            tr[table[i]] = i
        s = [11, 10, 3, 8, 4, 6]
        xor = 177451812
        add = 8728348608
        r = 0
        for i in range(6):
            r += tr[bvid[s[i]]] * 58 ** i
        return (r - add) ^ xor

    def video_list(self, mid, csvfpath):
        """
        抓取某用户所有的视频（链接）信息
        :param mid:  用户的mid（用户id）
        :param csvfpath: csv存储路径，用于存储该用户所有视频信息
        :return:
        """
        template = 'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp'

        #mid = 122592901  # 232472043
        home = template.format(mid=mid, page=1)
        resp = requests.get(home, headers=self.headers, cookies=self.cookies)
        count = resp.json()['data']['page']['count']
        ps = resp.json()['data']['page']['ps']
        page_max = int(count / ps) + 1
        print('该用户共有 {} 个视频'.format(count))

        with open(csvfpath, 'a+', encoding='utf-8', newline='') as csvf:
            fieldnames = ['author', 'bvid', 'aid', 'mid', 'created', 'length', 'comment', 'description', 'pic', 'play',
                          'subtitle', 'title']
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader()
            for page in range(1, page_max + 1):
                home2 = template.format(mid=mid, page=page)
                resp2 = requests.get(home2, headers=self.headers, cookies=self.cookies)
                videos = resp2.json().get('data').get('list').get('vlist')
                if videos:
                    for video in videos:
                        data = dict()
                        data['aid'] = video.get('aid')
                        data['author'] = video.get('author')
                        data['bvid'] = video.get('bvid')
                        data['comment'] = video.get('comment')
                        data['created'] = video.get('created')
                        data['description'] = video.get('description')
                        data['mid'] = video.get('mid')
                        data['pic'] = 'https:' + video.get('pic')
                        data['mid'] = video.get('mid')
                        data['play'] = video.get('play')
                        data['subtitle'] = video.get('subtitle')
                        data['length'] = video.get('length')
                        data['title'] = video.get('title')
                        writer.writerow(data)
                else:
                    return


        print('该用户相关视频信息请查看{}'.format(csvfpath))


    def comments(self, aid, csvfpath):
        """
        抓取某视频的所有评论
        :param aid: B站视频链接内的aid号
        :param csvfpath: csv存储路径，用于存储该用户所有视频信息
        :return:
        """
        #aid = 44384851  # 上面的aid

        template = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={oid}&sort=2'
        url = template.format(oid=aid, page=1)
        resp = requests.get(url, headers=self.headers, cookies=self.cookies)
        acount = resp.json()['data']['page']['acount']
        size = resp.json()['data']['page']['size']
        page_max = int(acount / size) + 1
        print('该视频共有 {} 个评论'.format(acount))

        with open(csvfpath, 'a+', encoding='utf-8', newline='') as csvf:
            fieldnames = ['content', 'device', 'like', 'rcount', 'ctime', 'avatar', 'level', 'sex', 'sign', 'uname',
                          'mid', 'oid', 'diag']
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader()
            for page in range(1, page_max + 1):
                url2 = template.format(oid=aid, page=page)
                resp2 = requests.get(url2, headers=self.headers, cookies=self.cookies)
                replies = resp2.json().get('data').get('replies')
                if replies:
                    for reply in replies:
                        data = dict()
                        data['content'] = reply.get('content').get('message')  # 评论内容
                        data['device'] = reply.get('content').get('device')  # 设备
                        data['like'] = reply.get('like')  # 喜欢数
                        data['rcount'] = reply.get('rcount')  # 互动数
                        data['ctime'] = reply.get('content').get('ctime')  # 创建时间
                        data['avatar'] = reply.get('member').get('avatar')  # 头像
                        data['level'] = reply.get('member').get('level_info').get('current_level')  # 评论者用户等级
                        data['sex'] = reply.get('member').get('sex')  # 评论者用户性别
                        data['sign'] = reply.get('member').get('sign')  # 评论者用户签名
                        data['uname'] = reply.get('member').get('uname')  # 评论者用户昵称
                        data['mid'] = reply.get('mid')  # 评论者用户mid
                        data['oid'] = reply.get('oid')  # 评论者用户oid
                        data['diag'] = '原评论'  # 一级评论
                        writer.writerow(data)

                        if data.get('rcount'):
                            for rreply in reply['replies']:
                                data['content'] = rreply.get('content').get('message')  # 评论内容
                                data['device'] = rreply.get('content').get('device')  # 设备
                                data['like'] = rreply.get('like')  # 喜欢数
                                data['rcount'] = rreply.get('rcount')  # 互动数
                                data['ctime'] = rreply.get('content').get('ctime')  # 创建时间
                                data['avatar'] = rreply.get('member').get('avatar')  # 头像
                                data['level'] = rreply.get('member').get('level_info').get('current_level')  # 评论者用户等级
                                data['sex'] = rreply.get('member').get('sex')  # 评论者用户性别
                                data['sign'] = rreply.get('member').get('sign')  # 评论者用户签名
                                data['uname'] = rreply.get('member').get('uname')  # 评论者用户昵称
                                data['mid'] = rreply.get('mid')  # 评论者用户mid
                                data['oid'] = rreply.get('oid')  # 评论者用户oid
                                data['diag'] = '原评论'  # 一级评论
                                writer.writerow(data)

                else:
                    return






