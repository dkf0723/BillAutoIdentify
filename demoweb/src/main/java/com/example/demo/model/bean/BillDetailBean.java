package com.example.demo.model.bean;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import lombok.Data;

@Data
public class BillDetailBean {
    private String number;
    private Integer column;
    private String productName;
    private Integer price;
    private Integer amount;
    private Integer totalColumnPrice;
}
