from api.views import SyncViewSet
from api.routes import CustomReadOnlyRouter

router = CustomReadOnlyRouter()
router.register(r'sync', SyncViewSet, basename='Custom')
