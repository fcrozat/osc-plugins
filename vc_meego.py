# vc_meego.py
# osc plugin to write MeeGo compliant .changes files
#
# Written by Frederic Crozat <fcrozat@novell.com>
# Copyright 2010 Novell, Inc.
# Released under the MIT/X11 license.
#


def do_vc_meego (self, subcmd, opts, *args):
    """${cmd_name}: update changes with MeeGo format

    ${cmd_usage}
    ${cmd_option_list}
    """
    import os
    import fnmatch
    from datetime import date
    import pwd
    import re

    if len(args) > 0:
        arg = args[0]
    else:
        arg = ""

    # set user's email if no mailaddr exists
    if not os.environ.has_key('mailaddr'):

        if arg and is_package_dir(arg):
            apiurl = store_read_apiurl(arg)
        else:
            apiurl = self.get_api_url()

        user = conf.get_apiurl_usr(apiurl)

        # work with all combinations of URL with or withouth the ending slas

        if conf.config['api_host_options'][apiurl].has_key('email'):
            mailaddr = conf.config['api_host_options'][apiurl] ['email']
        else:
            try:
                mailaddr = get_user_data(apiurl, user, 'email')[0]
            except Exception, e:
                sys.exit('%s\nget_user_data(email) failed. Try env mailaddr= ....\n' % e)
    else:
        mailaddr = os.environ.get('mailaddr');

    realname = pwd.getpwuid(os.getuid()).pw_gecos

    re_spec_version = re.compile('^(Version:\s*)(\S*)', re.IGNORECASE)
    for spec_file in fnmatch.filter(os.listdir('.'),'*.spec'):
        fin = open(spec_file, 'r')
        version = ""
        for line in fin.readlines():
            match = re_spec_version.match(line)
            if match:
                version = " - " + match.group(2)
                break

    for file in fnmatch.filter(os.listdir('.'),'*.changes'):
        with open (file, "r+") as f:
            old = f.read()
            f.seek(0)
#                * dow mmm dd yyyy Name Goes Here <your@email.com> - [version]"
            f.write ("* " + date.today().strftime("%a %b %d %Y")+ " " + realname
                     + " <" +mailaddr + ">"+ version + "\n" + old)

#            self.do_vc (subcmd, opts, *args)

