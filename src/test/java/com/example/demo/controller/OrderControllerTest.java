package com.example.demo.controller;

import com.example.demo.model.Order;
import com.example.demo.service.OrderService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class OrderControllerTest {

    @InjectMocks
    private OrderController orderController;

    @Mock
    private OrderService orderService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testGetAllOrders() {
        Order order1 = new Order();
        Order order2 = new Order();
        List<Order> orders = Arrays.asList(order1, order2);
        when(orderService.getAllOrders()).thenReturn(orders);

        List<Order> result = orderController.getAllOrders();

        assertEquals(2, result.size());
        verify(orderService, times(1)).getAllOrders();
    }

    @Test
    void testGetOrder() {
        Order order = new Order();
        when(orderService.getOrderById(anyLong())).thenReturn(order);

        Order result = orderController.getOrder(1L);

        assertNotNull(result);
        verify(orderService, times(1)).getOrderById(1L);
    }

    @Test
    void testPlaceOrder() {
        Order order = new Order();
        when(orderService.placeOrder(any())).thenReturn(order);

        Order result = orderController.placeOrder(order);

        assertNotNull(result);
        verify(orderService, times(1)).placeOrder(order);
    }

    @Test
    void testCancelOrder() {
        doNothing().when(orderService).cancelOrder(anyLong());

        orderController.cancelOrder(1L);

        verify(orderService, times(1)).cancelOrder(1L);
    }
}