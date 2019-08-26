# coding=utf-8

import os
import sys
import time
import subprocess
import mysql.connector


def main():
    file_list = []
    log_list = []
    finished_list = []
    time_step = 1
    file_ext = ['.mkv', '.avi', '.mp4']
    newfolder = 'newfolder/'
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="",
        passwd="",
        database="",
        use_unicode=True,
        charset="utf8"
    )
    
    mycursor = mydb.cursor()
    
    reload(sys)
    sys.setdefaultencoding('utf-8')    
    
    while True:    
        command_all = 'find . -maxdepth 2 -type f' # find all files.
        command = 'find . -maxdepth 2 -mmin -' + str(time_step) + ' -type f' # find files modified within 1 min.
        command_finished_all = 'find ./' + newfolder + ' -type f' # find files finished converting
        command_finished = 'find ./' + newfolder + ' -mmin -' + str(time_step) + ' -type f' # find files finished converting
        
        try:
            result_all = subprocess.check_output(command_all, shell=True)
            result = subprocess.check_output(command, shell=True)
            result_finished_all = subprocess.check_output(command_finished_all, shell=True)
            result_finished = subprocess.check_output(command_finished, shell=True)
            result_list_all = result_all.splitlines()
            result_list = result.splitlines()
            result_list_finished_all = result_finished_all.splitlines()
            result_list_finished = result_finished.splitlines()
            result_urls = []
            remove_urls = []
            # print(result_list_finished_all, result_list_finished)
            
            for url in result_list_all:
                if not url in result_list and newfolder not in url :
                    result_urls.append(url)
            
            for url in result_urls:
                for ext in file_ext:
                    if ext in url.lower():
                        if not url in file_list: file_list.append(url)
                        break
            
            for url in result_list_finished_all:
                if not url in result_list_finished :
                    remove_urls.append(url)
            
            # print(remove_urls)
            for url in file_list:
                if url in log_list : continue
                filename = url.split('/')[-1]
                qry = "SELECT `title` FROM `films` WHERE `download_url` LIKE '%" + filename + "%' "
                mycursor.execute(qry)
                myresult = mycursor.fetchall()
                
                if myresult:
                    title = myresult[0]
                    title = title[0].replace('film indir', '').replace('Film indir', '').replace('film Indir', '').replace('Film Indir', '').replace(u'ücretsiz', '').replace(u'Türkçe', '').replace(u'tek link', '').replace('1080p', '').replace(u'Dublaj', '').replace('indir', '').replace(':', ' ')
                else:
                    title = filename
                
                flag_continue = False
                for old_file in result_list_finished_all:
                    if filename in old_file : flag_continue = True
                log_list.append(url)
                for remove_url in remove_urls:
                    if filename in remove_url: os.system('rm -rf ' + url)
                if flag_continue == True : continue
                
                codec_cmd = '''ffmpeg -i ''' + url + ''' -vcodec libx264 -acodec aac -vf "drawtext=text=\'''' + title + '''\':x=w-tw:y=h-th:fontsize=24:fontcolor=white" -c:a copy ''' + newfolder + filename + ''' 2>/dev/null '''
                print(codec_cmd)
                os.system(codec_cmd)
            
            # print(file_list)
        except subprocess.CalledProcessError as e:
            pass
        
        time.sleep(time_step * 60) # Delay for 1 minute (60 seconds).


if __name__ == '__main__':
    main()