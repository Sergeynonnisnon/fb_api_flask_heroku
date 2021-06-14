
import time
from settings import FB_access_token, FB_id_groop, chanelSlack, FB_app_id, FB_app_secret, creator_post_skip
import facebook
from bd import DB
from slack_api import Bot
print("""create by Sergey Tokarev nonnisnon@gmail.com""")

class FB_API:

    def __init__(self, FB_access_token, FB_id_groop):
        self.Bot = Bot(chanelSlack)
        self.DB = DB()
        self.FB_id_groop = FB_id_groop
        #self.app_token = facebook.GraphAPI().get_app_access_token(app_id=FB_app_id, app_secret=FB_app_secret)
        #print(self.app_token)
        self.access_token = FB_access_token

        self.graph = facebook.GraphAPI(access_token=self.access_token , version="8.0")

    def _get_all_records(self):
        response = self.graph.get_object(id=self.FB_id_groop,
                                         fields='feed{from,id,message,comments{message,comments}}')
        feed = response.get('feed')
        data = feed.get('data')
        append_data_in_db = []
        for records in data:
            for i in records:
                if i == 'id':

                    recordsid = records.get(i)
                    if self.DB.check_post(record={'id_post': recordsid, 'id_creator': records.get('from').get('id')}):
                        link = f"https://www.facebook.com/groups/{recordsid.replace('_', '/permalink/')}"
                        print('post go to slack')
                        self.Bot.send_msg_Slack_new_post(
                            namegroop=self.get_name_group(),
                            link=link)

                if i == 'comments':

                    comments = records.get(i).get('data')

                    for comment in comments:


                        if comment.get('comments') is not None:
                            append_data_in_db.append([recordsid, comment.get('id'), 0])
                            for podcomment in (comment.get('comments').get('data')):
                                append_data_in_db.append([recordsid, comment.get('id'), podcomment.get('id')])

                        else:
                            append_data_in_db.append([recordsid, comment.get('id'), 0])
        print(f'comments count {len(append_data_in_db)}')

        return append_data_in_db

    def get_name_group(self):
        name_group = self.graph.get_object(id=self.FB_id_groop, fields='name')
        return name_group.get('name')

    def check_if_records_in_db(self):
        data = self._get_all_records()

        for i in data:

            row = i
            row.append(0)

            check = self.DB.check_comments(row)

            if check is True:

                if row[2] == 0:
                    comment = row[1]
                else:
                    comment = row[2]
                link = f"https://www.facebook.com/groups/{row[0].replace('_', '/permalink/')}?comment_id={comment}"

                if self.check_if_coments_is_admin(row):
                    self.Bot.send_msg_Slack_new_comment(
                        namegroop=self.get_name_group(),
                        link=link)
                    print('comment go to slack')

    def check_if_coments_is_admin(self, row):
        if row[2] == 0:

            id = str(row[0]) + '/comments'
            creator = self.graph.get_object(id=id, fields='id,comments,from')
            # print(creator)
            for data in creator.get('data'):
                if data.get('id') == row[1]:

                    id_creator = data.get('from').get('id')
                    if id_creator in creator_post_skip:
                        self.DB.update_bd_comments(record=row)
                        return False
                    else:
                        return True

        else:

            id = str(row[0]) + '/comments'
            creator = self.graph.get_object(id=id, fields='id,comments{from,id},from')

            for data in creator.get('data'):
                if data.get('id') == row[1]:

                    for comments in data.get('comments').get('data'):

                        if comments.get('id') == row[2]:
                            id_creator = comments.get('from').get('id')
                            if id_creator in creator_post_skip:
                                self.DB.update_bd_comments(record=row)
                                return False
                            else:
                                return True


def main():
    FB_API(FB_access_token, FB_id_groop).check_if_records_in_db()
    time.sleep(60)
    main()


if __name__ == '__main__':
    main()
