from netbox.api.routers import NetBoxRouter
from .views import *

router = NetBoxRouter()
router.register('hardwarelifecycle', HardwareLifecycleViewSet)
router.register('license', LicenseViewSet)
router.register('licenseassignment', LicenseAssignmentViewSet)
router.register('sku', SupportSKUViewSet)
router.register('supportcontract', SupportContractViewSet)
router.register('supportcontractassignment', SupportContractAssignmentViewSet)
router.register('vendor', VendorViewSet)
urlpatterns = router.urls
