import { Duration, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as fs from 'fs';
import { PolicyDocument } from 'aws-cdk-lib/aws-iam';


export class KinesisScalingWorkflow extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const targetShardCountCaclulatorLambda = new lambda.Function(this, 'CalculateTargetShardCountLambda', {
      functionName: 'CalculateTargetShardCountLambda',
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset('../lambda'),
      handler: 'kinesis_target_shard_calculator_lambda.lambda_handler'
    });
    const state_definition_template = fs.readFileSync('../step_function/state_definition.json').toString();
    const stateMachineRole = new iam.Role(this, 'KinesisScalingWorkflowRole', {
      assumedBy: new iam.ServicePrincipal('states.amazonaws.com'),
      description: 'Role for KinesisScalingWorkflow',
    });

    stateMachineRole.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: ['kinesis:DescribeStreamSummary', 'kinesis:UpdateShardCount'],
      resources: ['*']
    }));

    stateMachineRole.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: ['lambda:InvokeFunction'],
      resources: [targetShardCountCaclulatorLambda.functionArn]
    }));

    const statMachineDefinition = state_definition_template.replace('${FUNCTION_ARN}', targetShardCountCaclulatorLambda.functionArn)
    const stateMachine = new sfn.CfnStateMachine(this, 'KinesisScalingWorkflow', {
      stateMachineName: 'KinesisScalingWorkflow',
      definitionString: statMachineDefinition,
      roleArn: stateMachineRole.roleArn,
    });


  }
}
