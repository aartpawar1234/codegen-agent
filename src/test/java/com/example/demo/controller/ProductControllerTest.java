package com.example.demo.controller;

import com.example.demo.model.Product;
import com.example.demo.service.ProductService;
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

class ProductControllerTest {

    @InjectMocks
    private ProductController productController;

    @Mock
    private ProductService productService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testGetAllProducts() {
        Product product1 = new Product();
        Product product2 = new Product();
        List<Product> products = Arrays.asList(product1, product2);
        when(productService.getAllProducts()).thenReturn(products);

        List<Product> result = productController.getAllProducts();

        assertEquals(2, result.size());
        verify(productService, times(1)).getAllProducts();
    }

    @Test
    void testGetProduct() {
        Product product = new Product();
        when(productService.getProductById(anyLong())).thenReturn(product);

        Product result = productController.getProduct(1L);

        assertNotNull(result);
        verify(productService, times(1)).getProductById(1L);
    }

    @Test
    void testCreateProduct() {
        Product product = new Product();
        when(productService.createProduct(any())).thenReturn(product);

        Product result = productController.createProduct(product);

        assertNotNull(result);
        verify(productService, times(1)).createProduct(product);
    }

    @Test
    void testUpdateProduct() {
        Product product = new Product();
        when(productService.updateProduct(anyLong(), any())).thenReturn(product);

        Product result = productController.updateProduct(1L, product);

        assertNotNull(result);
        verify(productService, times(1)).updateProduct(1L, product);
    }

    @Test
    void testDeleteProduct() {
        doNothing().when(productService).deleteProduct(anyLong());

        productController.deleteProduct(1L);

        verify(productService, times(1)).deleteProduct(1L);
    }

    @Test
    void testGetProductNotFound() {
        when(productService.getProductById(anyLong())).thenThrow(new RuntimeException("Product not found"));

        Exception exception = assertThrows(RuntimeException.class, () -> {
            productController.getProduct(1L);
        });

        assertEquals("Product not found", exception.getMessage());
    }

    @Test
    void testGetProductByName() {
        String productName = "Test Product";
        Product product = new Product();
        when(productService.getProductByName(productName)).thenReturn(product);

        Product result = productController.getProductByName(productName);

        assertNotNull(result);
        verify(productService, times(1)).getProductByName(productName);
    }
}