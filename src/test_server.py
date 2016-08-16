# -*- coding: utf-8 -*-

import pytest

MSG_TABLE = [


]

@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_send_msg(msg)