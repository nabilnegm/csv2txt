# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 21:16:34 2020

"""

import pandas as pd
import numpy as np
import io
import os

def convert(path):
    ''' parameters: 
            path : string describing the path to the csv
        returns
            data : list of lists of data
            skills : list of lists of skills
    '''
    cv = pd.read_csv(path, header=None)
    data = []
    skills = []
    for index, row in cv.iterrows():
        if row[0] == 'headline' or row[0] == 'assessment' or row[0] == 'years of experience' or row[2] == 'None' or str(row[2]).replace('\t', '').replace('\n', '') == '':
            continue
        elif row[0] == 'last update' or row[0] == 'summary' or row[0] == 'relocation status' or row[0] == 'employment eligibility' or row[0] == 'publication' :
            data.append(['ignore', 'ignore', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
        elif row[0] == 'additional information':
            if str(row[2]).replace('\t', ' ').replace('\n', ' ').find('skill') != -1:
                skills.append(['skills', 'processing', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
            else:
                continue
        elif row[0] == 'work experience':
            if row[1] == 'work experience':
                continue
            elif row[1] == 'title':
                data.append(['experience', 'company_job_title', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
            elif row[1] == 'company':
                data.append(['experience', 'company_name', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
            elif row[1] == 'location':
                data.append(['experience', 'company_location', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
            elif row[1] == 'duration':
                data.append(['experience', 'period_in_company', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
            elif row[1] == 'description':
                data.append(['experience', 'company_job_desc', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
        elif row[0] == 'title':
            data.append(['experience', 'company_job_title', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
        elif row[0] == 'location':
            data.append(['personal_info', 'address', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
        elif row[0] == 'education':
            if row[1] == 'location' or row[1] == 'duration':
                continue
            elif row[1] == 'title':
                data.append(['education', 'education_field', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
            elif row[1] == 'school':
                data.append(['education', 'education_uni', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
        elif row[0] == 'skill':
            skills.append(['skills', 'processing', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
        elif row[0] == 'mail':
            if row[2].find('@') != -1:
                data.append(['personal_info', 'email', str(row[2]).replace('\t', ' ').replace('\n', ' ')])
        elif row[0] == 'certification':
            if row[1] == 'date':
                continue
            elif row[1] == 'title' or row[1] == 'description':
                data.append(['education', 'certificates', str(row[2]).replace('\t', ' ').replace('\n', ' ')])

    return data, skills

def print_data_to_file(data, data_file):
    ''' parameter:
            data: a list of lists containing data or skills
            data_file: path to text file
        prints to text file
        
    '''
    with io.open(data_file, 'w', encoding='utf8') as file:       
        for i in data:
            file.write(i[0] + '\t' + i[1] + '\t' + i[2] + '\n')
        file.close()


def looping_all_files(path):
    ''' main function
        parameters:
            path to folder containing the csvs
        calls print_data_to_file method
        no return
    ''' 
    data_list = []
    skills_list = []
    counter = 0
    f_counter = 0
    for f in os.listdir(path):
        counter+=1
        if counter ==1000:
            print_data_to_file(data_list,'./data_files/data_'+str(f_counter+10000)+'.txt')
            print_data_to_file(skills_list,'./skills_files/skills_'+str(f_counter+3500)+'.txt')
            f_counter+=1
            counter = 0
            data_list = []
            skills_list = []
            
        data,skills = convert(os.path.join(path,f))
        for i in data:
            data_list.append(i)
        for i in skills:
            skills_list.append(i)
    
    
    print('  done  ')
    
    
    
if __name__ == '__main__':
    looping_all_files('./folder')


