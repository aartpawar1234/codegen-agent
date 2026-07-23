package com.example.demo.service;

import com.example.demo.model.Order;
import com.example.demo.model.Product;
import com.example.demo.repository.OrderRepository;
import com.example.demo.repository.ProductRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Arrays;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class OrderServiceTest {

    @InjectMocks
    private OrderService orderService;

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private ProductRepository productRepository;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testGetAllOrders() {
        when(orderRepository.findAll()).thenReturn(Arrays.asList(new Order(), new Order()));

        assertEquals(2, orderService.getAllOrders().size());
        verify(orderRepository, times(1)).findAll();
    }

    @Test
    void testGetOrderById() {
        Order order = new Order();
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

        assertEquals(order, orderService.getOrderById(1L));
        verify(orderRepository, times(1)).findById(1L);
    }

    @Test
    void testPlaceOrder_HappyPath() {
        Product product = new Product();
        product.setId(1L);
        product.setPrice(100.0);
        product.setQuantity(10);

        Order order = new Order();
        order.setProductId(1L);
        order.setQuantity(2);

        when(productRepository.findById(1L)).thenReturn(Optional.of(product));
        when(orderRepository.save(any(Order.class))).thenReturn(order);
        when(productRepository.save(any(Product.class))).thenReturn(product);

        Order placedOrder = orderService.placeOrder(order);

        assertEquals(200.0, placedOrder.getTotalPrice());
        assertEquals(8, product.getQuantity()); // stock should be decremented
        verify(orderRepository, times(1)).save(order);
        verify(productRepository, times(1)).save(product);
    }

    @Test
    void testPlaceOrder_ProductNotFound() {
        Order order = new Order();
        order.setProductId(1L);
        order.setQuantity(2);

        when(productRepository.findById(1L)).thenReturn(Optional.empty());

        IllegalArgumentException thrown = assertThrows(IllegalArgumentException.class, () -> {
            orderService.placeOrder(order);
        });
        assertEquals("Product not found", thrown.getMessage());
    }

    @Test
    void testPlaceOrder_NotEnoughStock() {
        Product product = new Product();
        product.setId(1L);
        product.setPrice(100.0);
        product.setQuantity(1);

        Order order = new Order();
        order.setProductId(1L);
        order.setQuantity(2);

        when(productRepository.findById(1L)).thenReturn(Optional.of(product));

        IllegalArgumentException thrown = assertThrows(IllegalArgumentException.class, () -> {
            orderService.placeOrder(order);
        });
        assertEquals("Not enough stock available", thrown.getMessage());
    }

    @Test
    void testCancelOrder() {
        doNothing().when(orderRepository).deleteById(1L);

        orderService.cancelOrder(1L);

        verify(orderRepository, times(1)).deleteById(1L);
    }
}