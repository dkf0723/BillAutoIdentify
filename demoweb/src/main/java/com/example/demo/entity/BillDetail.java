package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "發票明細檔")
@IdClass(BillDetail.class)
public class BillDetail {
    @Id
    @Column(name = "發票號碼",length = 18,nullable= false)
    private String number;

    @Id
    @Column(name = "項次",nullable = false)
    private Integer column;

    @Column(name = "品名",length = 50,nullable = false)
    private String productName;

    @Column(name = "單價",nullable = false)
    private Integer price;

    @Column(name = "數量",nullable = false)
    private Integer amount;

    @Column(name = "金額",nullable = false)
    private Integer totalColumnPrice;
}
