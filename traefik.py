import argparse
import json
from pathlib import Path


class TraefikPlugin(object):
    def __init__(self):
        self.app_path = Path()
        self.network_name = Path("./NETWORK")
        self.settings = {
            "enabled": False,
            "name": "",
            "port": 5000,
            "domains": []
        }
        parser = argparse.ArgumentParser(description="Traefik <=> Dokku interfacer")
        parser.add_argument("--app_name", required=True)
        parser.add_argument("--dokku_root", required=True)
        parser.add_argument("--enable_proxy", help="Enable the proxy for the app", action="store_true")
        parser.add_argument("--disable_proxy", help="Disable the proxy for the app", action="store_true")
        parser.add_argument("--build_config", help="Build the config for the app", action="store_true")
        parser.add_argument("--update_domains", help="Update the list of Domains", action="store_true")
        parser.add_argument("--update_domains_action")
        parser.add_argument("--get_enabled", action="store_true")
        parser.add_argument("--domain", help="The domains to update", action="append")

        args = parser.parse_args()
        self.check_config(dokku_root=args.dokku_root, app_name=args.app_name)
        if args.enable_proxy:
            self.settings["enabled"] = True
        elif args.disable_proxy:
            self.settings["enabled"] = False
        elif args.get_enabled:
            print(self.settings["enabled"])
        elif args.build_config:
            self.build_config()
        elif args.update_domains:
            self.update_domains(domains=args.domain, action=args.update_domains_action)
        self.write_config()

    def check_config(self, dokku_root, app_name):
        self.app_path = Path(dokku_root).joinpath(app_name)
        config_file = self.app_path.joinpath("traefik.json")
        if self.app_path.exists():
            if not config_file.exists():
                config_file.touch()
                with config_file.open("w") as f:
                    self.settings["name"] = app_name
                    self.settings["domains"].append("")
                    json.dump(self.settings, f)
            else:
                with config_file.open() as f:
                    self.settings = json.load(f)
                    self.settings["name"] = app_name
        else:
            print("App does not exist")

    def write_config(self):
        config_file = self.app_path.joinpath("traefik.json")
        with config_file.open("w") as f:
            json.dump(self.settings, f)

    def print_info_1(self, message):
        print("-----> {}".format(message))

    def print_info_2(self, message):
        print("=====> {}".format(message))

    def build_config(self):
        if not self.app_path.joinpath("LABELS").exists():
            self.app_path.joinpath("LABELS").touch()
        with self.app_path.joinpath("LABELS").open("w") as f:
            net_name = ""
            with self.network_name.open("r") as nnf:
                net_name = nnf.read().rstrip()
            f.writelines([
                "traefik.enabled={}".format(self.settings["enabled"]),
                "traefik.{name}.frontend.rule=$Host:{hosts}".format(
                    name=self.settings["name"],
                    hosts=",".join(self.settings["domains"])
                ),
                "traefik.{name}.port={port}".format(
                    name=self.settings["name"],
                    port=self.settings["port"]
                ),
                "traefik.docker.network={network_name}".format(network_name=net_name)
            ])

    def update_domains(self, domains, action):
        print(action, domains)
        if action == "set":
            self.settings["domains"] = domains
        elif action == "add":
            self.settings["domains"].append(domains)
        elif action == "remove":
            [self.settings["domains"].remove(domain) for domain in domains]
        elif action == "clear":
            self.settings["domains"] = []
        else:
            print("Wrong action {}".format(action))


if __name__ == '__main__':
    TraefikPlugin()
