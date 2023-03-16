package com.example.demo.model.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "客戶主檔" )
public class Customer {
    @Id
    @Column(name = "統一編號",length = 30,nullable= false)
    private String taxIdNumber;

    @Column(name = "買受人",length = 30,nullable = false)
    private String buyer;

    @Column(name = "地址",length = 50,nullable = false)
    private String address;

}
