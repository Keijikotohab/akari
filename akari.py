import glob
import os
import urllib.request as libreq

import arxiv

from Akari.engine.summarize import BertSum
from Akari.utils.url_utils import get_fields
from Akari.utils.url_utils import get_id_list
from Akari.utils.url_utils import remove_nonrequired_paper
from Akari.utils.url_utils import save_sum_and_config
from Akari.web.build import web_builder


ID_LIST_DIR = './tmp/id_list'
PRESUM_DIR = './tmp/presum'
CONF_DIR = './tmp/conf'
SUM_DIR = './tmp/results'

def dir_checker(*args):
    for d in args:
        if not os.path.exists(d):
            os.mkdir(d)

if __name__ == '__main__':
    # get paper data from arXiv.
    # to get the newest papers, we search rss directory and get the newest data.
    # first, request to the rss directory.
    fields = get_fields() # list of field names.

    # set the tmp directory.
    dir_checker('./tmp', ID_LIST_DIR, PRESUM_DIR, CONF_DIR, SUM_DIR)

    # get id list from rss directory.
    for field in fields:
        outf = os.path.join(ID_LIST_DIR, field + '_tmp.txt')
        url = "http://export.arxiv.org/rss/" + field
        data = '\n'.join(get_id_list(url))
        with open(outf, 'wt') as f:
            f.write(data)

    # read the list file and get summaries.
    # if the 'update' column is not the previous day, then the file
    # will not be stored in pre-summary directory.
    for id_list in glob.glob(os.path.join(ID_LIST_DIR, '*.txt')):
        with open(id_list) as f:
            ids = [id.strip('\n') for id in f.readlines()]

        # send request to arxiv.
        data_before = arxiv.query(id_list=ids)
        data_after = remove_nonrequired_paper(data_before)

        # save title, summary and some other data as json format.
        # title format of saved pre-sum file is
        # '<field>_<paper_id>.presum.txt' and
        # '<field>_<paper_id>.config.json'
        save_sum_and_config(data_after, sum_outd=PRESUM_DIR, conf_outd=CONF_DIR)

    # run summarizarion.
    summarizer = BertSum()
    summarizer.set_input(in_dir=PRESUM_DIR)
    summarizer.summarize('bert') # 'mass' as optional.
    summarizer.save(outd=SUM_DIR)

    # build the html file or website to send to slack channel.
    # it is not implemented now.
    web_builder()
