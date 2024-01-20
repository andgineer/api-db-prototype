from typing import Any, Dict

import six
from connexion.frameworks.flask import FlaskJSONProvider

from openapi_server.models.base_model import Model


class JSONEncoder(FlaskJSONProvider):  # type: ignore
    """JSON encoder for Connexion with support for marshmallow schemas."""

    include_nulls = False

    def default(self, o: Any) -> Dict[str, Any]:
        """Convert object to dict."""
        if not isinstance(o, Model):
            return FlaskJSONProvider.default(self, o)  # type: ignore
        dikt = {}
        for attr, _ in six.iteritems(o.openapi_types):
            value = getattr(o, attr)
            if value is None and not self.include_nulls:
                continue
            attr = o.attribute_map[attr]
            dikt[attr] = value
        return dikt
