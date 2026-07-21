#!/usr/bin/env python3
"""Generate llms.txt from docs.json navigation + api-reference/openapi.json."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_URL = "https://docs.rovax.io"
out = []
W = out.append


# ---------- frontmatter / mdx parsing ----------
def read_page(slug):
    path = os.path.join(ROOT, slug + ".mdx")
    if not os.path.isfile(path):
        return None
    raw = open(path, encoding="utf-8").read()
    fm, body = {}, raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            fm = parse_fm(raw[3:end])
            body = raw[end + 4:]
    heads = []
    for line in body.splitlines():
        m = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if m:
            t = re.sub(r"[`*]", "", m.group(2)).strip()
            t = re.sub(r"<[^>]+>", "", t).strip()
            if t:
                heads.append((len(m.group(1)), t))
    return {"fm": fm, "headings": heads, "body": body}


def parse_fm(text):
    """Minimal YAML front-matter reader: scalars, quoted strings, block scalars."""
    fm, lines, i = {}, text.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in ("|", ">", "|-", ">-"):
            block, i = [], i + 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            fm[key] = " ".join(x for x in block if x)
            continue
        if val.startswith('"') and not val.endswith('"'):
            buf, i = [val[1:]], i + 1
            while i < len(lines) and not lines[i].rstrip().endswith('"'):
                buf.append(lines[i].strip())
                i += 1
            if i < len(lines):
                buf.append(lines[i].rstrip()[:-1].strip())
                i += 1
            fm[key] = " ".join(x for x in buf if x)
            continue
        fm[key] = val.strip('"').strip("'")
        i += 1
    return fm


def clean(text, limit=400):
    if not text:
        return ""
    text = re.sub(r"<br\s*/?>", " ", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[*`]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit].rstrip() + ("…" if len(text) > limit else "")


# ---------- navigation walk ----------
docs = json.load(open(os.path.join(ROOT, "docs.json"), encoding="utf-8"))
ENDPOINT_RE = re.compile(r"^(GET|POST|PUT|PATCH|DELETE)\s+/")


def emit_pages(pages, depth, seen):
    for item in pages:
        if isinstance(item, str):
            if ENDPOINT_RE.match(item):
                continue
            emit_page(item, depth, seen)
        elif isinstance(item, dict):
            title = item.get("group", "")
            if title:
                W("")
                W(f"{'#' * min(depth, 6)} {title}")
            root = item.get("root")
            if root:
                emit_page(root, depth + 1, seen)
            emit_pages(item.get("pages", []), depth + 1, seen)


def emit_page(slug, depth, seen):
    if slug in seen:
        return
    seen.add(slug)
    page = read_page(slug)
    path_part = "" if slug == "index" else ("en" if slug == "en/index" else slug)
    url = f"{DOCS_URL}/{path_part}" if path_part else DOCS_URL
    if page is None:
        W(f"- [{slug}]({url}) — MISSING FILE (referenced in navigation)")
        return
    title = clean(page["fm"].get("title") or slug, 120) or slug
    desc = clean(page["fm"].get("description"), 300)
    W(f"- [{title}]({url})" + (f" — {desc}" if desc else ""))
    h2 = [t for lvl, t in page["headings"] if lvl == 2]
    if h2:
        W(f"  - Sections: {'; '.join(h2[:14])}")


def walk_language(lang_node):
    seen = set()
    for tab in lang_node.get("tabs", []):
        name = tab.get("tab", "")
        W("")
        W(f"## {name}")
        if "groups" in tab:
            emit_pages(tab["groups"], 3, seen)
        elif "pages" in tab:
            emit_pages(tab["pages"], 3, seen)
    return seen


# ---------- header ----------
W("# Rovax.io Documentation")
W("")
W("> Rovax.io is an AI Agent platform for customer support, sales, and multichannel")
W("> automation. You build Agents (identity, prompt, model, tools, knowledge), connect")
W("> them to channels (WhatsApp, Instagram, Widget, Telegram, Slack), orchestrate them")
W("> with Workflows and Squads, hand conversations to humans in the Inbox, and drive")
W("> everything programmatically through a REST API.")
W("")
W("Documentation: https://docs.rovax.io")
W("Application:   https://app.rovax.io")
W("API base URL:  https://api.rovax.io")
W("Support:       contato@rovax.io")
W("")
W("Languages: pt-BR is served at the root path (/...), English at /en/...")
W("Product concepts are identical across both; this file lists both trees.")
W("")
W("This file is generated from docs.json (navigation), the page front matter of every")
W("MDX file, and api-reference/openapi.en.json (the OpenAPI 3 contract).")
W("It has two parts:")
W("  Part 1 — Documentation map: every published page, its description, and its sections.")
W("  Part 2 — API reference: every endpoint with parameters, bodies, responses, and schemas.")
W("")

# ---------- part 1 ----------
W("")
W("=" * 79)
W("PART 1 — DOCUMENTATION MAP")
W("=" * 79)

langs = docs["navigation"]["languages"]
for lang in langs:
    code = lang.get("language")
    label = "Portuguese (pt-BR) — served at /" if code == "pt-BR" else "English — served at /en/"
    W("")
    W("-" * 79)
    W(f"# {label}")
    W("-" * 79)
    walk_language(lang)

anchors = docs["navigation"].get("global", {}).get("anchors", [])
if anchors:
    W("")
    W("-" * 79)
    W("# External links")
    W("-" * 79)
    W("")
    for a in anchors:
        href = a.get("href", "")
        if href.startswith("/"):
            href = DOCS_URL + href
        W(f"- {a.get('anchor')}: {href}")
    W("- Support email: contato@rovax.io")

# ---------- part 2 ----------
spec = json.load(open(os.path.join(ROOT, "api-reference", "openapi.en.json"), encoding="utf-8"))
info = spec.get("info", {})
comps = spec.get("components", {})
schemas = comps.get("schemas", {})

W("")
W("")
W("=" * 79)
W("PART 2 — API REFERENCE")
W("=" * 79)
W("")
W(f"API: {info.get('title')} (version {info.get('version')})")
for s in spec.get("servers", []):
    W(f"Server: {s.get('url')}")
if info.get("description"):
    W("")
    for line in info["description"].strip().splitlines():
        W(line.rstrip())
W("")

# auth
W("## Authentication")
W("")
for name, sc in comps.get("securitySchemes", {}).items():
    W(f"- Scheme `{name}`: type={sc.get('type')} in={sc.get('in')} name={sc.get('name')}")
    if sc.get("description"):
        W(f"  {clean(sc['description'], 300)}")
W("")
W("Send the key on every request unless an endpoint is marked as public:")
W("  x-api-key: YOUR_API_KEY")
W("Keys are created at https://app.rovax.io/developers")
W("")

# conventions
W("## Conventions")
W("")
W("- Resource IDs are UUIDs; timestamps are ISO 8601.")
W("- List endpoints accept page, limit, order and return a pagination object")
W("  (page, limit, total, total_pages). Default page=1, limit=20, max limit=100.")
W("- Successful responses wrap the payload in a data key.")
W("- Errors return an error object: { code, message, status }.")
W("- Rate limit headers: X-RateLimit-Limit, X-RateLimit-Remaining,")
W("  X-RateLimit-Reset, Retry-After.")
W("")

# scopes
scopes = set()
for path_item in spec["paths"].values():
    for op in path_item.values():
        if not isinstance(op, dict):
            continue
        for sec in op.get("security", []) or []:
            for vals in sec.values():
                scopes.update(vals or [])
if scopes:
    W("## Scopes in use")
    W("")
    W("  " + ", ".join(sorted(scopes)))
    W("")

# shared parameters
if comps.get("parameters"):
    W("## Reusable parameters")
    W("")
    for name, p in comps["parameters"].items():
        sch = p.get("schema", {})
        bits = [f"in={p.get('in')}", f"type={sch.get('type', '?')}"]
        if sch.get("format"):
            bits.append(f"format={sch['format']}")
        if sch.get("default") is not None:
            bits.append(f"default={sch['default']}")
        if sch.get("enum"):
            bits.append("enum=" + "|".join(map(str, sch["enum"])))
        if sch.get("minimum") is not None:
            bits.append(f"min={sch['minimum']}")
        if sch.get("maximum") is not None:
            bits.append(f"max={sch['maximum']}")
        if p.get("required"):
            bits.append("required")
        W(f"- {name} ({p.get('name')}): {', '.join(bits)}")
        if p.get("description"):
            W(f"  {clean(p['description'], 200)}")
    W("")


# schema rendering helpers
def ref_name(ref):
    return ref.rsplit("/", 1)[-1]


def type_of(sch):
    if not isinstance(sch, dict):
        return "any"
    if "$ref" in sch:
        return ref_name(sch["$ref"])
    for key in ("allOf", "oneOf", "anyOf"):
        if key in sch:
            return f"{key}[" + ", ".join(type_of(s) for s in sch[key]) + "]"
    t = sch.get("type", "object" if "properties" in sch else "any")
    if t == "array":
        return f"array<{type_of(sch.get('items', {}))}>"
    extra = []
    if sch.get("format"):
        extra.append(sch["format"])
    if sch.get("enum"):
        extra.append("enum: " + "|".join(map(str, sch["enum"])))
    return t + (f" ({', '.join(extra)})" if extra else "")


def render_props(sch, indent, depth=0):
    if not isinstance(sch, dict):
        return
    if "$ref" in sch:
        W(f"{indent}{ref_name(sch['$ref'])} (see Schemas)")
        return
    if sch.get("type") == "array":
        items = sch.get("items", {})
        if "$ref" in items:
            W(f"{indent}array of {ref_name(items['$ref'])}")
        else:
            render_props(items, indent, depth)
        return
    props = sch.get("properties")
    if not props:
        if sch.get("description"):
            W(f"{indent}{clean(sch['description'], 200)}")
        return
    required = set(sch.get("required", []))
    for pname, p in props.items():
        flag = " [required]" if pname in required else ""
        line = f"{indent}- {pname}: {type_of(p)}{flag}"
        if isinstance(p, dict) and p.get("description"):
            line += f" — {clean(p['description'], 160)}"
        W(line)
        if depth < 1 and isinstance(p, dict) and p.get("properties"):
            render_props(p, indent + "  ", depth + 1)


# endpoints grouped by tag
tag_order = [t["name"] for t in spec.get("tags", [])]
by_tag = {}
for path, item in spec["paths"].items():
    for method, op in item.items():
        if method.startswith("x-") or not isinstance(op, dict):
            continue
        tags = op.get("tags") or ["Other"]
        by_tag.setdefault(tags[0], []).append((method.upper(), path, op, item))
for t in by_tag:
    if t not in tag_order:
        tag_order.append(t)

W("## Endpoint index")
W("")
W(f"Total: {sum(len(v) for v in by_tag.values())} operations across {len(by_tag)} groups.")
W("")
for tag in tag_order:
    ops = by_tag.get(tag)
    if not ops:
        continue
    W(f"{tag}:")
    for method, path, op, _ in sorted(ops, key=lambda x: (x[1], x[0])):
        W(f"  {method:6} {path:52} {clean(op.get('summary', ''), 80)}")
    W("")

W("")
W("## Endpoints in detail")
W("")
for tag in tag_order:
    ops = by_tag.get(tag)
    if not ops:
        continue
    W("")
    W("-" * 79)
    W(f"### {tag}")
    W("-" * 79)
    tag_desc = next((t.get("description") for t in spec.get("tags", []) if t["name"] == tag), None)
    if tag_desc:
        W(clean(tag_desc, 400))
    for method, path, op, item in sorted(ops, key=lambda x: (x[1], x[0])):
        W("")
        W(f"{method} {path}")
        if op.get("summary"):
            W(f"  Summary: {clean(op['summary'], 200)}")
        if op.get("description"):
            W(f"  Description: {clean(op['description'], 700)}")
        if op.get("operationId"):
            W(f"  operationId: {op['operationId']}")
        sec = op.get("security", None)
        if sec == []:
            W("  Auth: none (public endpoint)")
        else:
            needed = sorted({s for d in (sec or []) for v in d.values() for s in (v or [])})
            W("  Auth: x-api-key" + (f" — scopes: {', '.join(needed)}" if needed else ""))
        params = (item.get("parameters") or []) + (op.get("parameters") or [])
        if params:
            W("  Parameters:")
            for p in params:
                if "$ref" in p:
                    W(f"    - {ref_name(p['$ref'])} (reusable, see above)")
                    continue
                sch = p.get("schema", {})
                bits = [type_of(sch)]
                if p.get("required"):
                    bits.append("required")
                if sch.get("default") is not None:
                    bits.append(f"default={sch['default']}")
                line = f"    - {p.get('name')} ({p.get('in')}): {', '.join(bits)}"
                if p.get("description"):
                    line += f" — {clean(p['description'], 160)}"
                W(line)
        rb = op.get("requestBody")
        if rb:
            content = rb.get("content", {})
            for ctype, cval in content.items():
                req = " [required]" if rb.get("required") else ""
                W(f"  Request body ({ctype}){req}:")
                render_props(cval.get("schema", {}), "    ")
                ex = cval.get("example")
                if ex is not None:
                    W("    Example: " + json.dumps(ex, ensure_ascii=False)[:600])
        resps = op.get("responses", {})
        if resps:
            W("  Responses:")
            for code, r in sorted(resps.items()):
                if "$ref" in r:
                    r = comps.get("responses", {}).get(ref_name(r["$ref"]), {})
                W(f"    - {code}: {clean(r.get('description', ''), 160) or '(no description)'}")
                for ctype, cval in (r.get("content") or {}).items():
                    sch = cval.get("schema", {})
                    if code.startswith("2"):
                        render_props(sch, "        ")
W("")

# schemas
W("")
W("-" * 79)
W("### Schemas")
W("-" * 79)
for name in sorted(schemas):
    sch = schemas[name]
    W("")
    W(f"{name}")
    if sch.get("description"):
        W(f"  {clean(sch['description'], 400)}")
    render_props(sch, "  ")
W("")

# ---------- write ----------
text = "\n".join(out).rstrip() + "\n"
open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(text)
print(f"lines={text.count(chr(10))} bytes={len(text)}")
