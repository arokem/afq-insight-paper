import argparse
import hashlib
import os.path as op
import requests


def download_url_to_file(url, output_fn, encoding='utf-8'):
    fn_abs = op.abspath(output_fn)
    base = op.splitext(fn_abs)[0]

    # check if file with *.md5 exists 
    if (op.isfile(base + '.md5')):
        with open(base + '.md5', 'r') as md5file:
            md5sum = md5file.read().replace('\n', '')
    else:
        md5sum = None
    # compare MD5 hash
    if (op.isfile(fn_abs) and hashlib.md5(open(fn_abs, 'rb').read()).hexdigest() == md5sum):
        print(f'File {op.relpath(fn_abs)} exists.')
    else:
        print(f'Downloading {url} to {op.relpath(fn_abs)}.')
        # Download from url and save to file
        with requests.Session() as s:
            download = s.get(url)
            with open(fn_abs, 'w') as fp:
                fp.write(download.content.decode(encoding))

        # Write MD5 checksum to file
        with open(base + '.md5', 'w') as md5file:
            md5file.write(hashlib.md5(open(fn_abs, 'rb').read()).hexdigest())


def main():
    description = 'Download datasets to test AFQ-Insight.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--dataset', required=True, type=str, choices={'all', 'als'})
    results = parser.parse_args() # collect cmd line args

    datasets = results.dataset
    if datasets == 'all':
        datasets = ['als']
    else:
        datasets = [datasets]

    urls_files = {
        'als': [
            {
                'url': 'https://github.com/yeatmanlab/Sarica_2017/raw/gh-pages/data/nodes.csv',
                'file': './data/raw/als_data/nodes.csv'
            },
            {
                'url': 'https://github.com/yeatmanlab/Sarica_2017/raw/gh-pages/data/subjects.csv',
                'file': './data/raw/als_data/subjects.csv'
            },
        ],
    }

    for dset_key in datasets:
        for dict_ in urls_files[dset_key]:
            download_url_to_file(dict_['url'], dict_['file'])


if __name__ == '__main__':
    main()
