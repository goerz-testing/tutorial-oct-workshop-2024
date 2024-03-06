import re
from pathlib import Path
import jinja2
import subprocess as sp

env = jinja2.Environment()

header_template_str = r"""# <!-- Autoheader begin -->
# <hr/>
# <div id="{{topid}}" style="text-align:center; font-size:16px">{{part_lbl}}.{{excs_nr}} {{currtitle}}</div>
# <hr/>
# <table style="width: 100%">
#   <tr>
#     <th rowspan="2" style="width:33%; text-align:center; font-size:16px">
{%- if prevnb|length %}
#         <a href="{{prevnb}}">$\\leftarrow$ previous notebook </a><br>
#         <a href="{{prevnb}}" style="font-size:13px">{{prevnbtitle}}</a>
{%- endif %}
#     </th>
#     <td style="width:33%; text-align:center; font-size:16px">
{%- if prevtpc|length %}
#         <a href="{{prevtpc}}">$\\uparrow$ previous part $\\uparrow$</a><br>
#         <a href="{{prevtpc}}" style="font-size:13px">{{prevtpctitle}}</a>
{%- endif %}
#     </td>
#     <th rowspan="2" style="width:33%; text-align:center; font-size:16px">
{%- if nxtnb|length %}
#         <a href="{{nxtnb}}">next notebook $\\rightarrow$</a><br>
#         <a href="{{nxtnb}}" style="font-size:13px">{{nextnbtitle}}</a>
{%- endif %}
#     </th>
#   </tr>
#   <tr style="width: 100%">
#     <td style="width:33%; text-align:center; font-size:16px">
{%- if nexttpc|length %}
#         <a href="{{nexttpc}}" style="font-size:13px">{{nexttpctitle}}</a><br>
#         <a href="{{nexttpc}}">$\\downarrow$ next part $\\downarrow$</a>
{%- endif %}
#     </td>
#   </tr>
# </table>
#
# <div style="text-align: right;font-size: 16px"><a href="{{jupyref}}">👉 {{'Python' if 'py_' in jupyref else 'Julia'}} version</a></div>
#
# ---
# <!-- Autoheader end -->
"""

header_template = env.from_string(header_template_str)

footer_template_str = r"""# <!-- Autofooter begin -->
#
# ---
#
# [⬆︎ jump to top](#{{topid}})
# <!-- Autofooter end -->
"""

footer_template = env.from_string(footer_template_str)


header_re = re.compile(
    r"#\s*<!-- Autoheader begin -->.*<!-- Autoheader end -->", re.S
)
footer_re = re.compile(
    r"#\s*<!-- Autofooter begin -->.*<!-- Autofooter end -->", re.S
)
top = re.compile(r"(#\s*jupyter:.*?---)", re.S)


def insert_header(ipytxt, header_txt):
    if header_re.search(ipytxt):
        # header already exists and must be replaced:
        processed_txt = header_re.sub(header_txt, ipytxt)
    else:
        # header does not exist. Inserting it:
        processed_txt = top.sub(f"\\1\\n\\n{header_txt}", ipytxt)
    return processed_txt


def insert_footer(ipytxt, footer_txt):
    if footer_re.search(ipytxt):
        # footer already exists and must be replaced:
        processed_txt = footer_re.sub(footer_txt, ipytxt)
    else:
        # footer does not exist. Inserting it:
        processed_txt = ipytxt + f"\n\n{footer_txt}"
    return processed_txt


exercise_re = re.compile(r"(py|jl)_exercise_(\d+)_(\d+)_")

for f in Path(".").glob("*exercise*"):
    print(f)
    m = exercise_re.search(str(f))
    print(m[0])
    print(m.groups())
    break

aux = re.compile(r"abc")
aux.sub("xyz", "abcdefghiyk")

exercise_re = re.compile(r"(py|jl)_exercise_(\d+)_(\d+)_")
title_re = re.compile(r"^\s*#\s*#\s*(\w.*)$", re.M)
ft_dct = {"jl": "Julia", "py": "Python"}


def _get_title(filename, ext):
    sp.run(
        ["jupytext", "--to", ext, "--output", f"dummy.1.{ext}", filename]
    )
    with open(f"dummy.1.{ext}", "r") as f:
        ipytxt = f.read()

    ex_m = exercise_re.search(str(filename))
    part_nr = int(ex_m[2])
    excs_nr = int(ex_m[3])

    title_m = title_re.search(ipytxt)
    if not title_m:
        raise Exception(
            f"No title found in part {part_nr} and ex nr. {excs_nr}"
        )
    return f"{'I'*part_nr}.{excs_nr} {title_m[1]}"


def _get_if_file_exists(ft, part_nr, excs_nr, ext):
    """Check if note exists with exists with
    filetype `ft`, part `part_nr` and exercise `excs_nr`"""
    f_dir = Path(".") / ft_dct[ft]
    ex_globs = list(f_dir.glob(f"{ft}_exercise_{part_nr}_{excs_nr}*"))

    if len(ex_globs) == 0:
        if excs_nr == 0:
            if len(list(f_dir.glob(f"{ft}_exercise_{part_nr-1}_*"))):
                ex_globs = [
                    sorted(f_dir.glob(f"{ft}_exercise_{part_nr-1}_*"))[-1]
                ]
            else:
                ex_globs = []
        elif part_nr != 0:
            ex_globs = list(f_dir.glob(f"{ft}_exercise_{part_nr+1}_{1}*"))

    if len(ex_globs) == 0:
        return "", ""
    elif len(ex_globs) == 1:
        title = _get_title(ex_globs[0], ext)
        return title, ex_globs[0].name
    else:
        raise FileNotFoundError(
            f"More than one file beginning with `{ft}_exercise_{part_nr}_{excs_nr}`"
        )


def get_header_txt(filename, title, ext):
    ex_m = exercise_re.search(str(filename))
    ft = ex_m[1]
    part_nr = int(ex_m[2])
    excs_nr = int(ex_m[3])

    prevnbtitle, prevnb = _get_if_file_exists(ft, part_nr, excs_nr - 1, ext)
    nextnbtitle, nxtnb = _get_if_file_exists(ft, part_nr, excs_nr + 1, ext)
    prevtpctitle, prevtpc = _get_if_file_exists(ft, part_nr - 1, excs_nr, ext)
    nexttpctitle, nexttpc = _get_if_file_exists(ft, part_nr + 1, excs_nr, ext)

    prevpart = part_nr - 1
    nextpart = part_nr + 1

    switch_ft = "jl" if ft == "py" else "py"
    jupyref = f"../{ft_dct[switch_ft]}/{Path(_get_if_file_exists(switch_ft, part_nr, excs_nr, ext)[1]).name}"
    return header_template.render(
        topid=f"navtitle_{part_nr}_{excs_nr}_{ext}",
        part_lbl=("I" * part_nr),
        excs_nr=excs_nr,
        prevnb=prevnb,
        nxtnb=nxtnb,
        prevtpc=prevtpc,
        nexttpc=nexttpc,
        prevpart=prevpart,
        nextpart=nextpart,
        currentpart=part_nr,
        jupyref=jupyref,
        currtitle=title,
        prevtpctitle=prevtpctitle,
        nexttpctitle=nexttpctitle,
        prevnbtitle=prevnbtitle,
        nextnbtitle=nextnbtitle,
    )


def get_footer_txt(filename, title, ext):
    ex_m = exercise_re.search(str(filename))
    part_nr = int(ex_m[2])
    excs_nr = int(ex_m[3])
    return footer_template.render(
        topid=f"navtitle_{part_nr}_{excs_nr}_{ext}",
    )


def write_jupynb(filename, ext):
    dummy_file = f"dummy.{ext}"
    sp.run(["jupytext", "--to", ext, "--output", dummy_file, filename])
    with open(dummy_file, "r") as f:
        ipytxt = f.read()

    title_m = title_re.search(ipytxt)
    if not title_m:
        raise Exception("No title found")

    header_txt = get_header_txt(filename, title_m[1], ext)
    ipytxt = insert_header(ipytxt, header_txt)
    footer_txt = get_footer_txt(filename, title_m[1], ext)
    ipytxt = insert_footer(ipytxt, footer_txt)
    with open(dummy_file, "w") as f:
        f.write(ipytxt)
    sp.run(["jupytext", "--to", "ipynb", "--output", filename, dummy_file])


for f in sorted(Path(".").glob("Python/*exercise*.ipynb")):
    write_jupynb(f, ext="py")

for f in sorted(Path(".").glob("Julia/*exercise*.ipynb")):
    write_jupynb(f, ext="jl")
