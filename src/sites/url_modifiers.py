import re
from urllib.parse import urlparse

import tldextract
from requests import Response

DEFAULT_URL_PATTERN = "\"(.*?)\""
CSS_URL_PATTERN = "\((.*?)\)"
LINK_ATTRIBUTES = ["href", "src", "srcSet"]


def replace_urls(
        domain: str,
        text: str,
        link_attr: str,
        server_domain: str,
        site_name: str,
        site_full_domain: str,
) -> str:
    pattern = re.compile(f"{link_attr}={DEFAULT_URL_PATTERN}")

    def replace_match(match) -> str:
        matched_group = match.group(1)

        # Leave link unchanged if its domain does not belong to origin site
        if domain not in urlparse(matched_group).netloc and urlparse(matched_group).scheme:
            return match.group(0)

        # Process case where bunch of links are placed in srcSet attribute
        if link_attr == "srcSet":
            modified_links = []
            for link in matched_group.split(", "):
                modified_links.append(f"{server_domain}/statistics/{site_name}/{link}")
            return f'srcSet="{", ".join(modified_links)}"'
        else:
            # Construct url from party site url, Ex: "/path/to/data/
            if not urlparse(matched_group).scheme and matched_group.startswith("/"):
                return f'{link_attr}="{server_domain}/statistics/{site_name}/{site_full_domain}{matched_group}"'

            # Construct url from party site url, Ex: "path/to/data/
            if not urlparse(matched_group).scheme:
                return f'{link_attr}="{server_domain}/statistics/{site_name}/{site_full_domain}/{matched_group}"'

            # Construct url from origin site url
            return f'{link_attr}="{server_domain}/statistics/{site_name}/{matched_group}"'
    return pattern.sub(replace_match, text)


def css_replace_urls(text: str, server_domain: str, site_name: str) -> str:
    pattern = re.compile(f"url{CSS_URL_PATTERN}")

    def replace_match(match):
        matched_group = match.group(1)
        return f"url({server_domain}/statistics/{site_name}/{matched_group})"
    return pattern.sub(replace_match, text)


def modify_links_in_response(server_domain: str, site_full_domain: str, site_name: str, response: Response) -> str:
    modified_content = response.text
    domain = tldextract.extract(site_full_domain).domain
    for link_attr in LINK_ATTRIBUTES:
        modified_content = replace_urls(
            domain=domain,
            text=modified_content,
            link_attr=link_attr,
            server_domain=server_domain,
            site_name=site_name,
            site_full_domain=site_full_domain,
        )
    modified_content = css_replace_urls(modified_content, server_domain, site_name)
    return modified_content


def build_full_origin_link(site_full_domain: str, original_link: str) -> str:
    if not urlparse(original_link).scheme and original_link.startswith("/"):
        return f"{site_full_domain}{original_link}"
    return original_link
