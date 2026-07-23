package com.example.demo.service;

import com.example.demo.model.Order;
import com.example.demo.model.Product;
import com.example.demo.repository.OrderRepository;
import com.example.demo.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OrderService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private ProductRepository productRepository;

    public List<Order> getAllOrders() {
        return orderRepository.findAll();
    }

    public Order getOrderById(Long id) {
        return orderRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Order not found"));
    }

    public Order placeOrder(Order order) {
        Product product = productRepository.findById(order.getProductId())
                .orElseThrow(() -> new IllegalArgumentException("Product not found"));

        if (!hasEnoughStock(product.getId(), order.getQuantity())) {
            throw new IllegalArgumentException("Not enough stock available");
        }

        double total = product.getPrice() * order.getQuantity();
        order.setTotalPrice(total);
        product.setQuantity(product.getQuantity() - order.getQuantity());
        productRepository.save(product);

        return orderRepository.save(order);
    }

    public boolean hasEnoughStock(Long productId, int requestedQuantity) {
        Product product = productRepository.findById(productId).orElseThrow(() -> new IllegalArgumentException("Product not found"));
        return product.getQuantity() >= requestedQuantity;
    }

    public void cancelOrder(Long id) {
        Order order = orderRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Order not found"));
        orderRepository.deleteById(id);
        // Restore stock logic should be implemented here.
    }
}