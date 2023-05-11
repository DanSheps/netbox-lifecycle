from netbox.api.routers import NetBoxRouter
from .views import *

router = NetBoxRouter()
router.register('hardwarelifecycle', HardwareLifecycleViewSet)
router.register('license', LicenseViewSet)
router.register('licenseassignment', LicenseAssignmentViewSet)
router.register('supportcontract', SupportContractViewSet)
router.register('supportcontractassignment', SupportContractDeviceAssignmentViewSet)
router.register('vendor', VendorViewSet)
urlpatterns = router.urls
