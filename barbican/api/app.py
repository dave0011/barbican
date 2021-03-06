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

"""
API application handler for Cloudkeep's Barbican
"""

import falcon

from barbican.api.resources import (VersionResource,
                                    SecretsResource, SecretResource,
                                    OrdersResource, OrderResource)
from barbican.common import config
from barbican.crypto.extension_manager import CryptoExtensionManager
from barbican.openstack.common import log


def create_main_app(global_config, **local_conf):
    """uWSGI factory method for the Barbican-API application"""

    config.parse_args()
    log.setup('barbican')

    # Crypto Plugin Manager
    crypto_mgr = CryptoExtensionManager(
        'barbican.crypto.extension',
        ['simple_crypto']  # TODO: grab this list from cfg
    )

    # Resources
    VERSIONS = VersionResource()
    SECRETS = SecretsResource(crypto_mgr)
    SECRET = SecretResource(crypto_mgr)
    ORDERS = OrdersResource()
    ORDER = OrderResource()

    wsgi_app = api = falcon.API()
    api.add_route('/', VERSIONS)
    api.add_route('/v1/{tenant_id}/secrets', SECRETS)
    api.add_route('/v1/{tenant_id}/secrets/{secret_id}', SECRET)
    api.add_route('/v1/{tenant_id}/orders', ORDERS)
    api.add_route('/v1/{tenant_id}/orders/{order_id}', ORDER)

    return wsgi_app
