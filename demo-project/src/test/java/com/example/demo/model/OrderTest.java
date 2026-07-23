import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OrderTest {

    @Test
    public void testOrderCreation() {
        Order order = new Order(1, "Product A", 2);
        assertEquals(1, order.getId());
        assertEquals("Product A", order.getProductName());
        assertEquals(2, order.getQuantity());
    }

    @Test
    public void testOrderQuantityEdgeCase() {
        Order order = new Order(2, "Product B", 0);
        assertEquals(0, order.getQuantity()); // Edge case: quantity is zero
    }
}