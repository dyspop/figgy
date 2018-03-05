"""Test the make module."""

import Configify
import os
import pytest
import json

path = 'tests/'
filename = 'config'
format = 'json'
outpath = '{p}{fn}.{fmt}'.format(p=path, fn=filename, fmt=format)
data = {'spam': 'ni', 'ham': 'eggs'}


def setup_module(module):
    """Set up any state specific to the execution of the given module."""
    pass


def teardown_module(module):
    """Tear down any state that was previously setup with a setup_module."""
    try:
        os.remove(outpath)
    except OSError:
        pass


def test_args_none():
    """Should return TypeError."""
    with pytest.raises(TypeError):
        Configify.make()


def test_arg_data_none_error():
    """Should return an error if the input data is bad."""
    bad_input_datas = [
        None, False, True,
        1, 0, 0.1, complex('j'),
        [], [0, 1], (), (0, 1),
        range(0), range(1),
        '', 'spam',
        b'', b'spam',
        bytearray(), bytearray(b'\xf0\xf1\xf2'),
        {}, {0, 1}
    ]
    with pytest.raises(TypeError):
        for bad_input_data in bad_input_datas:
            Configify.make(data=bad_input_data)


def test_get_gets_dict():
    """Should get a dict when we supply the get argument."""
    assert isinstance(Configify.make(data=data, get=True), dict)


def test_arg_filename_blank_returns_config():
    """Should get something called 'config' if there's no argument."""
    assert 'config' in list(Configify.make(data=data, get=True).keys())[0]


def test_arg_filename_supplied_returns_arg_in_returned_dict():
    """Should get dict with first key returning the input filename."""
    assert 'spam' in list(Configify.make(
        data=data, get=True, filename='spam').keys())[0].split('.')[0]


def test_args_filename_and_path_concat_in_returned_dict():
    """We should be combining the args for the file write destination."""
    assert outpath.split('.')[0] == list(
        Configify.make(
            data=data, get=True, filename=filename, path=path
        ).keys())[0].split('.')[0]


def test_file_creation_args_minimal_viable():
    """We should get a file created so long as we supply data."""
    Configify.make(data=data)
    assert os.path.exists(outpath)



# def test_file_is_written():
#     """We should write a file if above tests pass."""

