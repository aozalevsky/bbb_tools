#!/usr/bin/env python3
#
# This script searches start/stop recording events
# in the events.xml file created by BigBlueButton
#
# Copyright (c) 2020, by Arthur Zalevsky <aozalevsky@gmail.com>
#
# The script is a free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# AffBio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with the script; if not, see
# http://www.gnu.org/licenses, or write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#

import argparse as ag
import xml.etree.ElementTree as ET


def get_args():
    """Parse cli arguments"""

    parser = ag.ArgumentParser(
        description='Search for start/stop events')

    parser.add_argument('-f',
                        type=str,
                        dest='fname',
                        metavar='EVENTS.XML',
                        help='events.xml file')

    parser.add_argument('-u', '--uuid',
                        type=str,
                        dest='uuid',
                        metavar='UUID',
                        help='UUID of the event. You can user either file name or uuid. File name overrides uuid.')

    args = parser.parse_args()
    args_dict = vars(args)
    return(args_dict)


def parse_file(fname):
    tree = ET.parse(fname)
    root = tree.getroot()
    return(root)


def search_events(root):
    events = root.findall(".//*[@eventname='RecordStatusEvent']")
    if len(events) == 0:
        print('Record was not started')
    else:
        en = len(events)
        for i in range(en):
            print('#' * 20)
            print('Event %d' % i)
            e = events[i]
            for t, v in e.items():
                print(t, v)
            for c in e.getchildren():
                if c.tag == 'userId':
                    print(c.tag, c.text, find_user_name(root, c.text))
                elif c.tag == 'status':
                    if c.text == 'true':
                        status = 'Started'
                    else:
                        status = 'Stopped'
                    print(c.tag, c.text, status)
                else:
                    print(c.tag, c.text)


def find_user_name(root, uid):
    events = root.findall(
        ".//*[@eventname='ParticipantJoinedEvent']/callername")

    if len(events) == 0:
        uname = 'Unknown user'
    else:
        # Better to check if all names are the same
        # to do
        uname = events[0].text

    return(uname)


def get_stop_event(timestampt='', userid='', status='false'):

    event = '  <event timestamp="" module="PARTICIPANT" eventname="RecordStatusEvent">\n'
    event += '    <userId>%s</userId>\n' % userid
    event += '    <status>%s</status>\n' % status
    event += '  </event>'

    return(event)


def print_stop_template():
    print('#' * 20)
    print('# To start/stop recording use the templated below')
    print('# Do not forget to set the correct timestamp,')
    print('# userId (e.g. w_jkbe7vlnnwgc)')
    print('# and status (true for start; false for stop)')
    stop = get_stop_event()
    print(stop)


if __name__ == '__main__':
    args = get_args()

    if args['fname'] is not None:
        fname = args['fname']
    elif args['uuid'] is not None:
        fname = '/var/bigbluebutton/recording/raw/%s/events.xml' % args['uuid']
    elif (args['fname'] is not None) and (args['uuid'] is not None):
        raise(Exception('You can not use filename and uuid simultaneously'))
    else:
        raise(Exception('Nor filename or uuid was specified'))

    print('Opening file: ')
    print(fname)
    root = parse_file(fname)

    search_events(root)
    print_stop_template()
