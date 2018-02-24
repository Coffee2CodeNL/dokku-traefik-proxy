import argparse
import re
from pathlib import Path
import json
from pprint import pprint

import jsonpickle as jsonpickle


class TraefikOptions(object):
    def __init__(self):
        self.domains = list()
        self.ports = list()
        self.out = {
            "domains": [],
            "ports": [],
            "enabled": False
        }

    def add_domain(self, domain):
        self.domains.append(domain)
        self.out["domains"] = self.domains

    def remove_domain(self, domain):
        self.domains.remove(domain)
        self.out["domains"] = self.domains

    def add_port(self, port):
        self.ports.append(port)
        self.out["ports"] = self.ports

    def remove_port(self, port):
        self.ports.remove(port)
        self.out["ports"] = self.ports

    def enable(self):
        self.out["enabled"] = True

    def disable(self):
        self.out["enabled"] = False

    def get_all(self):
        return self.out


class TraefikPlugin(object):
    def __init__(self):
        self.settings = dict()
        parser = argparse.ArgumentParser(description="Traefik <=> Dokku interfacer")
        parser.add_argument("--app_name", required=True)
        parser.add_argument("--dokku_root", required=True)
        parser.add_argument("--build_config", help="Build the config for the app", action="store_true")
        parser.add_argument("--post_create", help="")
        args = parser.parse_args()
        if args.build_config:
            self.build_config(dokku_root=args.dokku_root, app_name=args.app_name)

    def print_info_1(self, message):
        print("-----> {}".format(message))

    def print_info_2(self, message):
        print("=====> {}".format(message))

    def build_config(self, dokku_root, app_name):
        app_path = Path(dokku_root).joinpath(app_name)
        if app_path.exists():
            app_path.joinpath("traefik.json").touch()


if __name__ == '__main__':
    TraefikPlugin()
