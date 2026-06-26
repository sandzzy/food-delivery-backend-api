class Roles:
    ADMIN = "admin"
    RESTAURANT_OWNER = "restaurant_owner"
    CUSTOMER = "customer"


class OrderStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus:
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod:
    CASH = "cash"
    CARD = "card"
    UPI = "upi"
    WALLET = "wallet"
