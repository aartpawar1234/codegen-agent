import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class OrderServiceTest {

    private OrderService orderService;
    private OrderRepository orderRepository;

    @BeforeEach
    public void setUp() {
        orderRepository = mock(OrderRepository.class);
        orderService = new OrderService(orderRepository);
    }

    @Test
    public void testCreateOrder() {
        Order order = new Order(1, "Product A", 2);
        when(orderRepository.save(order)).thenReturn(order);
        Order createdOrder = orderService.createOrder(order);
        assertEquals(order, createdOrder);
    }

    @Test
    public void testCreateOrderWithNull() {
        assertThrows(IllegalArgumentException.class, () -> {
            orderService.createOrder(null);
        });
    }
}