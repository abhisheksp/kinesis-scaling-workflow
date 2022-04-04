#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { KinesisScalingWorkflow } from '../lib/cdk-stack';

const app = new cdk.App();
new KinesisScalingWorkflow(app, 'KinesisScalingWorkflow', {});
