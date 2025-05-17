class AgentRoutingError(Exception):
    """Raised when the routing logic fails to determine intent"""
    pass

class SupplierDiscoveryError(Exception):
    """Raised when supplier scraping fails"""
    pass

class EmailDraftingError(Exception):
    """Raised when email generation fails"""
    pass
