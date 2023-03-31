package com.example.demo.model.bean;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import lombok.Data;

@Data
public class BillPictureBean {
    private String billNumber;
    private String picture;
}
