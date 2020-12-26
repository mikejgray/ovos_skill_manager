from ovos_skills_manager.skill_entry import SkillEntry
from ovos_skills_manager.appstores import AbstractAppstore
from ovos_skill_installer import download_extract_zip
from tempfile import gettempdir
from os.path import join
from os import walk
import json


def get_ovos_skills(parse_github=False, skiplist=None):
    skiplist = skiplist or []
    path = join(gettempdir(), "ovos")
    dl_url = "https://github.com/OpenVoiceOS/OVOS-appstore/archive/main.zip"
    download_extract_zip(dl_url, path,  join(path, "ovos-appstore.zip"))
    for root, folders, files in walk(path):
        files = [f for f in files if f.endswith(".json")]
        for f in files:
            with open(join(root, f)) as j:
                data = json.load(j)
                if data["url"] in skiplist:
                    continue
                yield SkillEntry.from_json(data,
                                           parse_github=parse_github)


class OVOSstore(AbstractAppstore):
    def __init__(self, parse_github=False):
        super().__init__("OVOS", parse_github)

    def get_skills_list(self, skiplist=None):
        skiplist = skiplist or []
        return get_ovos_skills(parse_github=self.parse_github,
                               skiplist=skiplist)
