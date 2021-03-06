# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc

from barbican.model.models import EncryptedDatum


class CryptoPluginBase(object):
    """Base class for Crypto plugins."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def encrypt(self, unencrypted, secret, tenant):
        """Encrypt unencrypted data in the context of the provided
        secret and tenant"""

    @abc.abstractmethod
    def decrypt(self, secret_type, secret, tenant):
        """Decrypt secret into secret_type in the context of the
        provided tenant"""

    @abc.abstractmethod
    def create(self, secret_type):
        """Create a new key."""

    @abc.abstractmethod
    def supports(self, secret_type):
        """Whether the plugin supports the specified secret type."""


class SimpleCryptoPlugin(CryptoPluginBase):
    """Insecure implementation of the crypto plugin."""

    #TODO: Use PyCrypto to aes encode secrets

    def __init__(self):
        self.supported_types = ['application/aes-256-cbc']

    def encrypt(self, unencrypted, secret, tenant):
        encrypted_datum = EncryptedDatum()
        encrypted_datum.cypher_text = 'encrypted-data'
        return encrypted_datum

    def decrypt(self, secret_type, secret, tenant):
        encrypted_datum = secret.encrypted_data
        return 'plain-data'

    def create(self, secret_type):
        return "insecure_key"

    def supports(self, secret_type):
        return secret_type in self.supported_types
