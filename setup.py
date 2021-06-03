#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 21:36:58 2021

@author: bs15ansj
"""
from setuptools import setup, find_packages
import os
from os.path import splitext
from glob import glob
from os.path import basename

import pip

pip.main(['install', 'Longbow @ git+https://github.com/pacilab/Longbow.git@master'])

setup(
    name='AmberPy',
    version='0.0.1',
    liscence='MIT',
    description=('A tool for setting up and performing molecular dynamics '
                 'simulations using Amber on the University of Leeds Arc HPC'),
    author='Alex St John',
    author_email='bs15ansj@leeds.ac.uk',
    url='https://github.com/pacilab/AmberPy.git',
    packages=find_packages(include=['amberpy', 'amberpy.*']),
    classifiers=[
         # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',

        'Programming Language :: Python :: 3.7',
        ],
    install_requires=['biopython',
                      'scikit-learn',
                     # 'Longbow @ git+https://github.com/pacilab/Longbow.git@master'
                      ],
    scripts=['amberpy/james']
)

 # Try and create the .amberpy with hosts.conf
try:

    # Setting up the .Longbow directory.
    if not os.path.isdir(os.path.expanduser('~/.amberpy')):
        print('Making hidden AmberPy directory in ~')
        os.mkdir(os.path.expanduser('~/.amberpy'))
        
    else:
        print('Directory already exists at "~/.amberpy" - Skipping')
    
    if not os.path.isfile(os.path.expanduser('~/.amberpy/hosts.conf')):
        
        username = input("Enter your Arc username: ")
        
        # Check username will work in connecting to arc3 and arc4
        from longbow.shellwrappers import sendtossh
        
        cmd = {}
        cmd['port'] = '22'
        cmd['user'] = username
        cmd['host'] = 'arc3'
        cmd["env-fix"] = "false"
        
        print(f'Running Longbow to check arc3 connection with username: {username}')
        sendtossh(cmd, ['ls'])
        print('Connection successful')
        cmd['host'] = 'arc4'
        print(f'Running Longbow to check arc4 connection with username: {username}')
        sendtossh(cmd, ['ls'])
        print('Connection successful')
        
        remoteworkdir = input('Enter the path to your /nobackup directory: ')
        
        cmd['host'] = 'arc3'
        print('Running Longbow to check that /nobackup directory exists on arc3')
        sendtossh(cmd, [f'touch {remoteworkdir}/tmp.txt'])
        sendtossh(cmd, [f'rm {remoteworkdir}/tmp.txt'])
        cmd['host'] = 'arc4'
        print('Running Longbow to check that /nobackup directory exists on arc4')
        sendtossh(cmd, [f'touch {remoteworkdir}/tmp.txt'])
        sendtossh(cmd, [f'rm {remoteworkdir}/tmp.txt'])
        
        
        print('Making AmberPy host configuration file in ~/.amberpy')
        HOSTFILE = open(os.path.expanduser('~/.amberpy/hosts.conf'), 'w+')
    
        HOSTFILE.write(
                    "[arc3-gpu]\n"
                    "host = arc3\n"
                    "cores = 0\n"
                    "arcsge-gpu = p100\n"
                    "scheduler = arcsge\n"
                    "modules = amber/20gpu\n"
                    "executable = pmemd.cuda_SPFP\n"
                    f"remoteworkdir = {remoteworkdir}\n"
                    f"user = {username}\n"
                    "\n"
                    "[arc3-cpu]\n"
                    "host = arc3\n"
                    "scheduler = arcsge\n"
                    "modules = amber\n"
                    "handler = mpirun\n"
                    "executable = pmemd.MPI\n"
                    f"remoteworkdir = {remoteworkdir}\n"
                    f"user = {username}\n"
                    "\n"
                    "[arc4-gpu]\n"
                    "host = arc4\n"
                    "cores = 0\n"
                    "arcsge-gpu = v100\n"
                    "scheduler = arcsge\n"
                    "modules = amber/20gpu\n"
                    "executable = pmemd.cuda_SPFP\n"
                    f"remoteworkdir = {remoteworkdir}\n"
                    f"user = {username}\n"
                    "\n"
                    "[arc4-cpu]\n"
                    "host = arc4\n"
                    "scheduler = arcsge\n"
                    "modules = amber\n"
                    "handler = mpirun\n"
                    "executable = pmemd.MPI\n"
                    f"remoteworkdir = {remoteworkdir}\n"
                    f"user = {username}\n"
                    "\n")

        HOSTFILE.close()


        
except IOError:
    
    print('AmberPy failed to create the host configuration file in '
          '"~/.amberpy/hosts.conf"')