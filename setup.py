from distutils.core import setup
setup(
  name = 'tureng',
  packages = ['tureng'],
  version = '0.1.001',
  license='gpl-3.0',
  description = 'Unofficial, basic python 3 tureng.com mobile API wrapper',
  author = 'Kadir Can Çetin',
  author_email = 'kadircancetinl@gmail.com',
  url = 'https://github.com/kadircancetin/tureng',
  download_url = 'https://github.com/kadircancetin/tureng/archive/v_01_001.tar.gz',
  keywords = ['tureng', 'türkçe', 'inglizce', 'translation', 'turkish', 'english'],
  install_requires=[
          'requests',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
