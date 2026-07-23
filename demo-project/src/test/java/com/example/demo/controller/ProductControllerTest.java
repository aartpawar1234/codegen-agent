package com.example.demo.controller;

import com.example.demo.model.Product;
import com.example.demo.service.ProductService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
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

        when(productService.getAllProducts(0, 10)).thenReturn(products);

        List<Product> result = productController.getAllProducts(0, 10);

        assertEquals(2, result.size());
        verify(productService, times(1)).getAllProducts(0, 10);
    }

    @Test
    void testGetProduct_HappyPath() {
        Product product = new Product();
        when(productService.getProductById(1L)).thenReturn(product);

        Product result = productController.getProduct(1L);

        assertNotNull(result);
        verify(productService, times(1)).getProductById(1L);
    }

    @Test
    void testGetProduct_NotFound() {
        when(productService.getProductById(anyLong())).thenThrow(new RuntimeException("Product not found"));

        Exception exception = assertThrows(RuntimeException.class, () -> {
            productController.getProduct(1L);
        });

        assertEquals("Product not found", exception.getMessage());
    }

    @Test
    void testCreateProduct() {
        Product product = new Product();
        when(productService.createProduct(any(Product.class))).thenReturn(product);

        Product result = productController.createProduct(product);

        assertNotNull(result);
        verify(productService, times(1)).createProduct(product);
    }

    @Test
    void testUpdateProduct() {
        Product product = new Product();
        when(productService.updateProduct(anyLong(), any(Product.class))).thenReturn(product);

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
    void testCheckStock_HappyPath() {
        when(productService.isInStock(1L, 5)).thenReturn(true);

        boolean result = productController.checkStock(1L, 5);

        assertTrue(result);
        verify(productService, times(1)).isInStock(1L, 5);
    }

    @Test
    void testCheckStock_NotInStock() {
        when(productService.isInStock(1L, 5)).thenReturn(false);

        boolean result = productController.checkStock(1L, 5);

        assertFalse(result);
        verify(productService, times(1)).isInStock(1L, 5);
    }
}