# -*- coding: utf-8 -*-

import time
import os
import traceback
from ftplib import FTP

#localfilelist = '/home/yixin/yxdata/ftp/update_migration.txt'
localdir = '/Users/samyzhang/Documents/xin/face_recognition/my_faces'
remotedir = '/home/wac/ngxin/ftp_upload'
print('The FTPupload programe is running...')


def getftpconnect():
    ftp_server = '121.69.75.194'
    username = 'wac'
    password = '8112whz'
    ftp = FTP()
    #ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect(ftp_server, 22)  # 连接
    ftp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
    print ftp.getwelcome()
    return ftp


def ftp_upload(ftp, remotefile, localfile):
    #f = open(localpath, "rb")
    #filename = os.path.split(localpath)[-1]
    try:
        #bufsize = 1024
        #localpath_file = os.listdir(localpath)
        #for filename in localpath_file:
        #fp = open(filename, 'rb')
        fp = open(localfile,'rb')
        ftp.storbinary('STOR ' + remotefile, fp)  # 上传文件
        ftp.set_debuglevel(0)
        fp.close()  # 关闭文件
        #ftp.quit()
        print('上传完成')

    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':


    while True:
        # if os.path.exists(localfilelist):
        #     with open(localfilelist, 'r') as file1:
        #         filelist = file1.readlines()  # 读取本地已有的文件列表
        #         filelist = map(str.strip, filelist)  # 过滤每一行的\n
        #         localfileset = set(filelist)
        # else:
        #     localfileset = set()
        #     # 建立传输通道
        try:
            ftptransport = getftpconnect()
            if not os.path.exists(remotedir):
                print ("不存在该目录，程序将主动创建")
                os.makedirs(remotedir)
            # remote_localfiles = os.listdir(localdir)  # 这个程序中比较的文件列表就在本地
            # remote_localfileset = set(remote_localfiles)
            # # 求差集,获得新文件列表
            # newfiles = remote_localfileset - localfileset
            # newfileslist = list(newfiles)
            # newfileslist.sort()  # 按顺序上传
            # time.sleep(10)  # 10s执行一次,顺便等待文件写完
            localdir_file = os.listdir(localdir)

            #with open(localfilelist, 'a') as locallist:
            for item in localdir_file:
                file_to_send = localdir + str(item)
                remotefile = remotedir + str(item)
                ftp_upload(ftptransport, remotefile, file_to_send)
                #locallist.write(str(item) + "\n")  # 把已经上传的文件追加到已下载记录中去

            ftptransport.quit()
        except Exception as e:
            traceback.print_exc()
            try:
                ftptransport.close()
            except:
                print('关闭有错')
