import argparse
import json
from pathlib import Path


class TraefikPlugin(object):
    def __init__(self):
        self.app_path = Path()
        self.settings = {
            "services": [
                {
                    "enabled": False,
                    "name": "default",
                    "port": 5000,
                    "domains": []
                }
            ]
        }
        parser = argparse.ArgumentParser(description="Traefik <=> Dokku interfacer")
        parser.add_argument("--app_name", required=True)
        parser.add_argument("--dokku_root", required=True)
        parser.add_argument("--build_config", help="Build the config for the app", action="store_true")
        parser.add_argument("--update_domains", help="Update the list of Domains", action="store_true")
        parser.add_argument("--update_domains_action")
        parser.add_argument("--domain", help="The domains to update", action="append")

        args = parser.parse_args()
        self.check_config(dokku_root=args.dokku_root, app_name=args.app_name)
        if args.build_config:
            self.build_config()
        elif args.update_domains:
            if args.update_domains_action == "set":
                self.update_domains(domains=args.domain, action=args.update_domains_action)
        self.write_config()

    def check_config(self, dokku_root, app_name):
        self.app_path = Path(dokku_root).joinpath(app_name)
        config_file = self.app_path.joinpath("traefik.json")
        if self.app_path.exists():
            if not config_file.exists():
                config_file.touch()
                with config_file.open("w") as f:
                    json.dump(self.settings, f)
            else:
                with config_file.open() as f:
                    self.settings = json.load(f)
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
        app_path = self.app_path
        if app_path.exists():
            app_path.joinpath("traefik.json").touch()

    def update_domains(self, domains, action):
        services = self.settings["services"]
        for service in services:
            if action == "set":
                service["domains"] = domains
            elif action == "add":
                service["domains"].append(domains)
            elif action == "remove":
                [service["domains"].remove(domain) for domain in domains]
            elif action == "clear":
                service["domains"] = []
            else:
                print("Wrong action {}".format(action))


if __name__ == '__main__':
    TraefikPlugin()
