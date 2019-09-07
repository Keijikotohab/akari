
import datetime
import json
import os
import urllib.request as libreq
import xml.etree.ElementTree as ET

from Akari.utils.usrs import USER




def get_fields(usr=None):
    if usr is not None:
        # read user's config
        usr_conf = USER(usr)
        return user_conf.fields
    else:
        return ['cs.CL']

def get_id_list(url=None):
    """request to specified url and get id list.

    Args:
        url (str): Url of the request.

    Returns:
        List: id list of papers which is to request
            to the arXiv.

    """
    with libreq.urlopen(url) as response:
        xml_string = response.read()

    pagef = ET.fromstring(xml_string)
    links = [list(i.attrib.values())[0] for i in pagef]

    # because links[0] and linkss[1] is not a paper-related
    # link, so we remove links[0] and links[1]
    links = links[2:]

    # now links is a list of links. Paper ids are
    # included at the last of their links.
    ids = [link.split('/')[-1] for link in links]
    return ids

def remove_nonrequired_paper(data_before):
    """Remove paper which is not updated the day before.

    Args:
        data_before(List[Dict[arxiv_response]]):
            List of Dictionary. Response of `arxiv` api.

    Returns:
        List[Dict[arxiv_response]]: List of dictionary.

    """
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday = datetime.datetime.strftime(yesterday, '%Y-%m-%d')
    ret = []
    for paper in data_before:
        if paper['updated'].split('T')[0] == yesterday:
            ret.append(paper)
    return ret

def save_sum_and_config(data_after, sum_outd, conf_outd, tokenlist=None):
    """save config and pre-sum."""
    if tokenlist is None:
        tokenlist = ['title', 'published', 'authors', 'arxiv_url']

    # save pre-sum and config json file.
    for paper in data_after:
        save_dict = {k:v for k,v in paper.items() if k in tokenlist}
        summary = paper['summary'].replace('\n', ' ')
        tag = paper['arxiv_primary_category']['term']
        file_id = paper['id'].split('/')[-1]
        name = tag + '_' + file_id
        # save summary file.
        with open(os.path.join(sum_outd, name + '.presum.txt'), "w") as f:
            f.write(summary)
        # link path to the pre_sum file into config file.
        save_dict['pre_sum'] = os.path.join(sum_outd, name + '.presum.txt')
        with open(os.path.join(conf_outd, name + 'config.json'), 'w') as f:
            json.dump(save_dict, f)
