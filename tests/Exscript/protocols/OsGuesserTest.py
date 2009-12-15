import sys, unittest, re, os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from Exscript.protocols.OsGuesser import OsGuesser
from StreamAnalyzerTest           import StreamAnalyzerTest

login_responses = {
'ios': '''

(Banner goes here)

testhost line 2 


at 'testhost.t' port 'tty2' from '10.0.0.1'

Username: test
Password:
testhost#''',

'junos': '''

(Banner goes here)


testhost (ttyp0)

login: test
Password: 

--- JUNOS 8.4R4.2 built 2008-05-21 08:47:52 UTC
user@testhost> ''',

'ios_xr': '''

(Banner goes here)

at 'testhost.t' port '/dev/vty1' from '10.0.0.1'

Username: sab
s/key 9796 en29000000
Password: 
RP/0/RP0/CPU0:testhost#''',

'shell': '''
telnet (testhost)






WARNING ! ! !  YOU ARE MONITORED
Access to this system is restricted to authorized uses only.
Any attempt to access this system without proper authority may result in prosecution.


Security System V 5.0

Authorized Login: test
test's Password: 
*******************************************************************************
* testhost                                                                    *
*                                                                             *
*  AIX 4.3.3                                                                  *
*                                                                             *
*******************************************************************************
Last unsuccessful login: Mon Mar 30 14:12:54 CEST 2009 on /dev/pts/102 from testhost.local
Last login: Mon Dec 14 08:38:37 CET 2009 on /dev/pts/109 from testhost.local

test@testhost:/home/test> ''',

'unknown': '''
user@testhost> ''',
}

class FakeConnection(object):
    def is_authenticated(self):
        return False

class OsGuesserTest(StreamAnalyzerTest):
    CORRELATE = OsGuesser

    def setUp(self):
        self.sa = OsGuesser(FakeConnection())

    def testConstructor(self):
        osg = OsGuesser(FakeConnection())
        self.assert_(isinstance(osg, OsGuesser))

    def testDataReceived(self):
        for os, response in login_responses.iteritems():
            osg = OsGuesser(FakeConnection())
            osg.data_received(response)
            self.assertEqual(osg.get('os'), os)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(OsGuesserTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite())

