import json
from pathlib import Path


FIELDS = {
    "description": "Description",
    "physical_address": "Physical Address",
    "dhcp_enabled": "DHCP Enabled",
    "ipv4_address": "IPv4 Address",
    "subnet_mask": "Subnet Mask",
    "default_gateway": "Default Gateway",
    "dns_servers": "DNS Servers"
}


def parse_ipconfig_text(text):
    adapters = []      
    current = None     

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if line.endswith(":") and ("adapter" in line.lower()):
            if current:
                adapters.append(current)

            current = {
                "adapter_name": line[:-1],   # A ":" nélkül
                "description": "",
                "physical_address": "",
                "dhcp_enabled": "",
                "ipv4_address": "",
                "subnet_mask": "",
                "default_gateway": "",
                "dns_servers": []
            }
            continue

        if not current:
            continue

        for key, label in FIELDS.items():
            if line.startswith(label):
                value = line.split(":", 1)[1].strip()

                if key == "dns_servers":
                    if value:
                        current["dns_servers"].append(value)
                else:
                    current[key] = value
                break

        if current and current["dns_servers"]:
            if line and line[0].isdigit():
                current["dns_servers"].append(line)

    if current:
        adapters.append(current)

    return adapters

def main():
    input_files = ["parser_input_a.txt", "parser_input_b.txt"]
    output = []

    for filename in input_files:
        file = Path(filename)
        if not file.exists():
            continue

        text = file.read_text(encoding="utf-8", errors="ignore")
        adapters = parse_ipconfig_text(text)

        output.append({
            "file_name": filename,
            "adapters": adapters
        })

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
