import os, re, shutil, json, glob, jsbeautifier, subprocess

def get_newest_app_dir(appdir):
    dir = os.listdir(appdir)
    matches = [item for item in dir if re.match(r'([0-9]+\.){3}[0-9]+', item)]
    matches.sort()
    newest_vivaldi = os.path.join(appdir, matches[-1])
    return newest_vivaldi

def get_newest_app_resource_dir(appdir):
    dir = os.listdir(appdir)
    matches = [item for item in dir if re.match(r'([0-9]+\.){3}[0-9]+', item)]
    matches.sort()
    newest_vivaldi = os.path.join(appdir, matches[-1], 'resources', 'vivaldi')
    return newest_vivaldi

def get_strings(fromfile):
    fixed = jsbeautifier.beautify_file(fromfile)
    matches=set()
    for line in fixed.split("\n"):
        for match in re.finditer("\"[^\"]*\"", line):
            matches.add(match.group(0))
        for match in re.finditer("'[^']*'", line):
            matches.add(match.group(0))
    listed = list(matches)
    listed.sort()
    return listed, fixed

def do_copy_crap(resources_loc):
    for jsvivfile in glob.glob(os.path.join(resources_loc, "*/*.js")):
        print(jsvivfile)
        strings, unminified = get_strings(jsvivfile)
        filename = os.path.sep.join(jsvivfile.split(os.path.sep)[7:])
        dirtofile = os.path.sep.join(jsvivfile.split(os.path.sep)[7:len(jsvivfile.split(os.path.sep))-1])
        newpath = os.path.join(OUT_STRINGS_DIR, dirtofile)
        newpath2 = os.path.join(OUT_SOURCES_DIR, dirtofile)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        if not os.path.exists(newpath2):
            os.makedirs(newpath2)
        with open(os.path.join(OUT_STRINGS_DIR,filename), "w", encoding="utf-8") as stringout:
            for matched in strings:
                stringout.write(matched.strip("\"").strip("'")+"\n")
        with open(os.path.join(OUT_SOURCES_DIR,filename), "w", encoding="utf-8") as unminout:
            unminout.write(unminified)
    for jsvivfile in glob.glob(os.path.join(resources_loc, "*.js")):
        print(jsvivfile)
        strings, unminified = get_strings(jsvivfile)
        filename = os.path.sep.join(jsvivfile.split(os.path.sep)[7:])
        with open(os.path.join(OUT_STRINGS_DIR,filename), "w", encoding="utf-8") as stringout:
            for matched in strings:
                stringout.write(matched.strip("\"").strip("'")+"\n")
        with open(os.path.join(OUT_SOURCES_DIR,filename), "w", encoding="utf-8") as unminout:
            unminout.write(unminified)

def get_flags(flag_user_data_dir):
    print("Flags "+flag_user_data_dir)
    with open(OUT_FLAGS_HTML, "w", encoding="utf-8") as stringout:
        with subprocess.Popen([os.path.join(VIVALDI_APP_DIR, "vivaldi.exe"), "--user-data-dir="+flag_user_data_dir, "--headless", "--disable-gpu", "--dump-dom", "chrome://flags"], stdout=subprocess.PIPE, universal_newlines=True) as p:
            for line in p.stdout:
                stringout.write(line)

def get_binfile_strings(binfile):
    print(binfile)
    strings=set()
    with subprocess.Popen(["strings.exe", binfile], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            if(len(line) > 6):
                cleanline = line.strip()
                if(cleanline.count(" ")>0):
                    strings.add(cleanline)
    listed = list(strings)
    listed.sort()
    with open(os.path.join(OUT_BINSTRS_DIR, binfile.split(os.path.sep)[-1]+".txt"), "w", encoding="utf-8") as stringout:
        for line in listed:
            stringout.write(line+"\n")

def do_bin_strings(app_dir):
    bindir = get_newest_app_dir(app_dir)
    get_binfile_strings(os.path.join(app_dir, "vivaldi.exe"))
    for binfile in glob.glob(os.path.join(bindir, "*")):
        get_binfile_strings(binfile)

def copy_non_js_source(src):
    print(src)
    filename = src.split(os.path.sep)[-1]
    dirtofile = os.path.sep.join(src.split(os.path.sep)[7:len(src.split(os.path.sep))-1])
    dst = os.path.join(OUT_SOURCES_DIR,dirtofile)
    if not (os.path.exists(dst)):
        os.makedirs(dst)
    shutil.copyfile(src, os.path.join(dst,filename))

def get_non_js_sources(resources_loc):
    for src in glob.glob(os.path.join(resources_loc, "*/*.css")):
        copy_non_js_source(src)
    for src in glob.glob(os.path.join(resources_loc, "*.css")):
        copy_non_js_source(src)
    for src in glob.glob(os.path.join(resources_loc, "*/*.html")):
        copy_non_js_source(src)
    for src in glob.glob(os.path.join(resources_loc, "*.html")):
        copy_non_js_source(src)
    for src in glob.glob(os.path.join(resources_loc, "*/*.svg")):
        copy_non_js_source(src)
    for src in glob.glob(os.path.join(resources_loc, "*.svg")):
        copy_non_js_source(src)

def main():
    resources_loc = get_newest_app_resource_dir(VIVALDI_APP_DIR)
    for dir in [OUT_STRINGS_DIR, OUT_BINSTRS_DIR, OUT_SOURCES_DIR]:
        print("Cleaning " + dir)
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
    do_copy_crap(resources_loc)
    do_bin_strings(VIVALDI_APP_DIR)
    get_non_js_sources(resources_loc)
    #get_flags(V_USER_DATA_DIR)

VIVALDI_APP_DIR = "C:\\Program Files\\Vivaldi\\Application"
V_USER_DATA_DIR = "C:\\Users\\me\\AppData\\Local\\Vivaldi\\test"
OUT_STRINGS_DIR = "C:\\path\\to\\output\\strings"
OUT_BINSTRS_DIR = "C:\\path\\to\\output\\appstrings"
OUT_SOURCES_DIR = "C:\\path\\to\\output\\sources"
OUT_FLAGS_HTML = "C:\\path\\to\\output\\flags.html"
main()
