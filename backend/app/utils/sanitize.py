import bleach

ALLOWED_TAGS = [
    'a','b','i','em','strong','u','p','ul','ol','li','br','span','blockquote','code','pre','h1','h2','h3','h4','h5','h6'
]
ALLOWED_ATTRS = {
    '*': ['class'],
    'a': ['href', 'title', 'target', 'rel'],
    'span': ['style'],
}
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def sanitize_html(html: str) -> str:
    if not html:
        return ''
    cleaned = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    return bleach.linkify(cleaned)