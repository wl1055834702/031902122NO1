#	coding=gbk
# ����
# ���ͳ���
# ʱ�䣺2021/11/12 0:07
# mysql���ݿ���������˿ڣ�3306�����ҷ������Ǵ�������״̬
# ��װpymysql��pip install pymysql
import pymysql
import threading
from settings import MYSQL_HOST, MYSQL_DB, MYSQL_PWD, MYSQL_USER


class DataManager():
    # ����ģʽ��ȷ��ÿ��ʵ����������һ������
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DataManager, "_instance"):
            with DataManager._instance_lock:
                DataManager._instance = object.__new__(cls)
                return DataManager._instance

        return DataManager._instance

    def __init__(self):
        # ��������
        self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PWD, database=MYSQL_DB, charset='utf8')

        # �����α�
        self.cursor = self.conn.cursor()

    def save_data(self, data):
        # ���ݿ����
        # (1)����һ����ʽ����sql���
        sql = 'insert into qiushi(author,funny_num,comment_num,content) values(%s,%s,%s,%s) '
        # (2)׼������
        # data = ('nancy','30','100','̫��Ц��')
        # (3)����
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print('��������ʧ��', e)
            self.conn.rollback()  # �ع�

    def __del__(self):
        # �ر��α�
        self.cursor.close()
        # �ر�����
        self.conn.close()
